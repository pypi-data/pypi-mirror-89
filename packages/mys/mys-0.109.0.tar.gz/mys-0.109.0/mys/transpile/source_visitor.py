import textwrap
from pathlib import Path
from ..parser import ast
from .utils import CompileError
from .utils import InternalError
from .utils import TypeVisitor
from .utils import is_integer_literal
from .utils import is_float_literal
from .utils import make_integer_literal
from .utils import make_float_literal
from .utils import INTEGER_TYPES
from .utils import Context
from .utils import BaseVisitor
from .utils import get_import_from_info
from .utils import params_string
from .utils import return_type_string
from .utils import CppTypeVisitor
from .utils import indent
from .utils import is_string
from .utils import METHOD_OPERATORS
from .definitions import is_method

def default_value(mys_type):
    if mys_type in INTEGER_TYPES:
        return '0'
    elif mys_type in ['f32', 'f64']:
        return '0.0'
    elif mys_type == 'Bool':
        return 'Bool(false)'
    elif mys_type == 'String':
        return 'String()'
    else:
        return 'nullptr'

def is_docstring(node, source_lines):
    if not isinstance(node, ast.Constant):
        return False

    if not isinstance(node.value, str):
        return False

    if not is_string(node, source_lines):
        return False

    return not node.value.startswith('mys-embedded-c++')

def has_docstring(node, source_lines):
    first = node.body[0]

    if isinstance(first, ast.Expr):
        return is_docstring(first.value, source_lines)

    return False

def create_class_init(class_name, member_names, member_types, member_values):
    params = []
    body = []

    for member_name, member_type in zip(member_names, member_types):
        if member_name.startswith('_'):
            value = default_value(member_type)
            body.append(f'this->{member_name} = {value};')
        else:
            params.append(f'{member_type} {member_name}')
            body.append(f'this->{member_name} = {member_name};')

    params = ', '.join(params)
    body = '\n'.join(body)

    return '\n'.join([
        f'{class_name}::{class_name}({params})',
        '{',
        indent(body),
        '}'
    ])

def create_class_del(class_name):
    return f'{class_name}::~{class_name}()\n{{\n}}'

def create_class_str(class_name):
    return (f'String {class_name}::__str__() const\n'
            '{\n'
            '    std::stringstream ss;\n'
            '    ss << *this;\n'
            '    return String(ss.str().c_str());\n'
            '}')

def create_class_format(class_name, member_names):
    members = [f'os << "{name}=" << obj.{name}' for name in member_names]
    members = indent(' << ", ";\n'.join(members))

    if members:
        members += ';'

    return '\n'.join([
        f'std::ostream& operator<<(std::ostream& os, const {class_name}& obj)',
        '{',
        f'    os << "{class_name}(";',
        members,
        '    os << ")";',
        '    return os;',
        '}'
    ])

def create_enum_from_integer(enum):
    code = f'{enum.type} enum_{enum.name}_from_value({enum.type} value)\n'
    code += '{\n'
    code += '    switch (value) {\n'

    for name, value in enum.members:
        code += f'    case {value}:\n'
        code += f'        return ({enum.type}){enum.name}::{name};\n'

    code += '    default:\n'
    code += '        throw ValueError("bad enum value");\n'
    code += '    }\n'
    code += '}'

    return code

class SourceVisitor(ast.NodeVisitor):

    def __init__(self,
                 module_levels,
                 module_hpp,
                 filename,
                 skip_tests,
                 namespace,
                 source_lines,
                 definitions,
                 module_definitions):
        self.module_levels = module_levels
        self.source_lines = source_lines
        self.module_hpp = module_hpp
        self.filename = filename
        self.skip_tests = skip_tests
        self.namespace = namespace
        self.forward_declarations = []
        self.add_package_main = False
        self.before_namespace = []
        self.context = Context()
        self.definitions = definitions
        self.module_definitions = module_definitions
        self.enums = []

        for name, functions in module_definitions.functions.items():
            self.context.define_function(name, functions)

        for name, trait_definitions in module_definitions.traits.items():
            self.context.define_trait(name, trait_definitions)

        for name, class_definitions in module_definitions.classes.items():
            self.context.define_class(name, class_definitions)

        for enum in module_definitions.enums.values():
            self.enums.append(self.visit_enum(enum))
            self.enums.append(create_enum_from_integer(enum))

    def visit_AnnAssign(self, node):
        return AnnAssignVisitor(self.source_lines,
                                self.context,
                                self.source_lines).visit(node)

    def visit_Module(self, node):
        body = [
            self.visit(item)
            for item in node.body
        ]

        return '\n\n'.join([
            '// This file was generated by mys. DO NOT EDIT!!!',
            f'#include "{self.module_hpp}"'
        ] + self.before_namespace + [
            f'namespace {self.namespace}',
            '{'
        ] + self.forward_declarations + self.enums + body + [
            '}',
            '',
            self.main()
        ])

    def main(self):
        if self.add_package_main:
            return '\n'.join([
                'void package_main(int argc, const char *argv[])',
                '{',
                f'    {self.namespace}::main(argc, argv);',
                '}',
                ''
            ])
        else:
            return ''

    def visit_ImportFrom(self, node):
        module, name, asname = get_import_from_info(node, self.module_levels)
        imported_module = self.definitions.get(module)

        if imported_module is None:
            raise CompileError(f"imported module '{module}' does not exist", node)

        if name.name.startswith('_'):
            raise CompileError(f"can't import private definition '{name.name}'", node)

        if name.name in imported_module.variables:
            self.context.define_global_variable(
                asname,
                imported_module.variables[name.name].type,
                node)
        elif name.name in imported_module.functions:
            self.context.define_function(asname,
                                         imported_module.functions[name.name])
        elif name.name in imported_module.classes:
            self.context.define_class(asname,
                                      imported_module.classes[name.name])
        else:
            raise CompileError(
                f"imported module '{module}' does not contain '{name.name}'",
                node)

        return ''

    def get_decorator_names(self, decorator_list):
        names = []

        for decorator in decorator_list:
            if isinstance(decorator, ast.Call):
                names.append(self.visit(decorator.func))
            elif isinstance(decorator, ast.Name):
                names.append(decorator.id)
            else:
                raise CompileError("decorator", decorator)

        return names

    def visit_enum(self, enum):
        members = []

        for name, value in enum.members:
            members.append(f"    {name} = {value},")

        self.context.define_enum(enum.name, enum.type)

        return '\n'.join([
            f'enum class {enum.name} : {enum.type} {{'
        ] + members + [
            '};'
        ])

    def visit_trait(self, name, node):
        body = []

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                pass
                # body.append(TraitMethodVisitor(name,
                #                                self.source_lines,
                #                                self.context,
                #                                self.filename).visit(item))
            elif isinstance(item, ast.AnnAssign):
                raise CompileError('traits can not have members', item)

        return '\n'.join(body)

    def visit_ClassDef(self, node):
        class_name = node.name
        members = []
        member_types = []
        member_names = []
        member_values = []
        method_names = []
        body = []

        decorator_names = self.get_decorator_names(node.decorator_list)

        if decorator_names == ['enum']:
            return ''
        elif decorator_names == ['trait']:
            return self.visit_trait(class_name, node)
        elif decorator_names:
            raise InternalError('invalid class decorator(s)', node)

        bases = []

        for base in node.bases:
            if not self.context.is_trait_defined(base.id):
                raise CompileError('trait does not exist', base)

            bases.append(f'public {base.id}')

        bases = ', '.join(bases)

        if not bases:
            bases = 'public Object'

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.context.push()

                if is_method(item.args):
                    body.append(MethodVisitor(class_name,
                                              method_names,
                                              self.source_lines,
                                              self.context,
                                              self.filename).visit(item))
                else:
                    raise CompileError("class functions are not yet implemented",
                                       item)

                self.context.pop()
            elif isinstance(item, ast.AnnAssign):
                member_name = self.visit(item.target)
                mys_type = TypeVisitor().visit(item.annotation)

                if not self.context.is_type_defined(mys_type):
                    raise CompileError(f"undefined type '{mys_type}'",
                                       item.annotation)

                member_type = CppTypeVisitor(self.source_lines,
                                             self.context,
                                             self.filename).visit(item.annotation)

                if item.value is not None:
                    member_value = ClassMemberValueVisitor(
                        self.source_lines,
                        self.context,
                        self.source_lines).visit(item)
                elif member_type in ['i8', 'i16', 'i32', 'i64']:
                    member_value = "0"
                elif member_type in ['u8', 'u16', 'u32', 'u64']:
                    member_value = "0"
                elif member_type in ['f32', 'f64']:
                    member_value = "0.0"
                elif member_type == 'String':
                    member_value = 'String()'
                elif member_type == 'bytes':
                    member_value = "Bytes()"
                elif member_type == 'bool':
                    member_value = "false"
                else:
                    member_value = 'nullptr'

                members.append(f'{member_type} {member_name};')
                member_types.append(member_type)
                member_names.append(member_name)
                member_values.append(member_value)

        if '__init__' not in method_names:
            body.append(create_class_init(class_name,
                                          member_names,
                                          member_types,
                                          member_values))

        if '__del__' not in method_names:
            body.append(create_class_del(class_name))

        if '__str__' not in method_names:
            body.append(create_class_str(class_name))

        body = '\n\n'.join(body) + '\n\n'
        body += create_class_format(class_name, member_names)

        return body

    def visit_FunctionDef(self, node):
        self.context.push()

        if node.returns is None:
            return_mys_type = None
        else:
            return_mys_type = TypeVisitor().visit(node.returns)

            if self.context.is_enum_defined(return_mys_type):
                return_mys_type = self.context.get_enum_type(return_mys_type)

        self.context.return_mys_type = return_mys_type

        function_name = node.name
        return_type = return_type_string(node.returns,
                                         self.source_lines,
                                         self.context,
                                         self.filename)
        params = params_string(function_name,
                               node.args.args,
                               self.source_lines,
                               self.context)
        body = []
        body_iter = iter(node.body)

        if has_docstring(node, self.source_lines):
            next(body_iter)

        for item in body_iter:
            body.append(indent(BodyVisitor(self.source_lines,
                                           self.context,
                                           self.filename).visit(item)))

        if function_name == 'main':
            self.add_package_main = True

            if return_type != 'void':
                raise CompileError("main() must not return any value", node)

            if params not in ['const std::shared_ptr<List<String>>& argv', 'void']:
                raise CompileError("main() takes 'argv: [string]' or no arguments",
                                   node)

            if params == 'void':
                body = [indent('\n'.join([
                    '(void)__argc;',
                    '(void)__argv;'
                ]))] + body
            else:
                body = [indent('auto argv = create_args(__argc, __argv);')] + body

            params = 'int __argc, const char *__argv[]'

        prototype = f'{return_type} {function_name}({params})'
        decorators = self.get_decorator_names(node.decorator_list)

        if 'test' in decorators:
            if self.skip_tests:
                code = ''
            else:
                parts = Path(self.module_hpp).parts
                full_test_name = list(parts[1:-1])
                full_test_name += [parts[-1].split('.')[0]]
                full_test_name += [function_name]
                full_test_name = '::'.join([part for part in full_test_name])
                code = '\n'.join([
                    '#if defined(MYS_TEST)',
                    '',
                    f'static {prototype}',
                    '{'
                ] + body + [
                    '}',
                    '',
                    f'static Test mys_test_{function_name}("{full_test_name}", '
                    f'{function_name});',
                    '',
                    '#endif'
                ])
        else:
            self.forward_declarations.append(prototype + ';')
            code = '\n'.join([
                prototype,
                '{'
            ] + body + [
                '}'
            ])

        self.context.pop()

        return code

    def visit_Expr(self, node):
        return self.visit(node.value) + ';'

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            if node.value.startswith('mys-embedded-c++-before-namespace'):
                self.before_namespace.append('\n'.join([
                    '/* mys-embedded-c++-before-namespace start */\n',
                    textwrap.dedent(node.value[33:]).strip(),
                    '\n/* mys-embedded-c++-before-namespace stop */']))
                return ''
            elif node.value.startswith('mys-embedded-c++'):
                return '\n'.join([
                    '/* mys-embedded-c++ start */\n',
                    textwrap.dedent(node.value[17:]).strip(),
                    '\n/* mys-embedded-c++ stop */'])

        raise CompileError("syntax error", node)

    def generic_visit(self, node):
        raise InternalError("unhandled node", node)

class MethodVisitor(BaseVisitor):

    def __init__(self, class_name, method_names, source_lines, context, filename):
        super().__init__(source_lines, context, filename)
        self._class_name = class_name
        self._method_names = method_names

    def validate_operator_signature(self, method_name, return_type, node):
        expected_return_type = {
            '__add__': self._class_name,
            '__sub__': self._class_name,
            '__iadd__': None,
            '__isub__': None,
            '__eq__': 'bool',
            '__ne__': 'bool',
            '__gt__': 'bool',
            '__ge__': 'bool',
            '__lt__': 'bool',
            '__le__': 'bool'
        }[method_name]

        if return_type != expected_return_type:
            raise CompileError(
                f'{method_name}() must return {expected_return_type}',
                node)

    def visit_FunctionDef(self, node):
        method_name = node.name

        if node.returns is None:
            self.context.return_mys_type = None
        else:
            self.context.return_mys_type = TypeVisitor().visit(node.returns)

        return_type = self.return_type_string(node.returns)

        if node.decorator_list:
            raise Exception("methods must not be decorated")

        self.context.define_variable('self', self._class_name, node.args.args[0])
        params = params_string(method_name,
                               node.args.args[1:],
                               self.source_lines,
                               self.context)
        self._method_names.append(method_name)

        if method_name in METHOD_OPERATORS:
            self.validate_operator_signature(method_name,
                                             self.context.return_mys_type,
                                             node)
            method_name = 'operator' + METHOD_OPERATORS[method_name]

        body = []
        body_iter = iter(node.body)

        if has_docstring(node, self.source_lines):
            next(body_iter)

        for item in body_iter:
            body.append(indent(BodyVisitor(self.source_lines,
                                           self.context,
                                           self.filename).visit(item)))

        body = '\n'.join(body)

        if method_name == '__init__':
            return '\n'.join([
                f'{self._class_name}::{self._class_name}({params})',
                '{',
                body,
                '}'
            ])
        elif method_name == '__del__':
            raise CompileError('__del__ is not yet supported', node)

        return '\n'.join([
            f'{return_type} {self._class_name}::{method_name}({params})',
            '{',
            body,
            '}'
        ])

    def generic_visit(self, node):
        raise InternalError("unhandled node", node)

class TraitMethodVisitor(BaseVisitor):

    def __init__(self, class_name, source_lines, context, filename):
        super().__init__(source_lines, context, filename)
        self._class_name = class_name

    def validate_operator_signature(self,
                                    method_name,
                                    params,
                                    return_type,
                                    node):
        expected_return_type = {
            '__add__': self._class_name,
            '__sub__': self._class_name,
            '__iadd__': 'void',
            '__isub__': 'void',
            '__eq__': 'bool',
            '__ne__': 'bool',
            '__gt__': 'bool',
            '__ge__': 'bool',
            '__lt__': 'bool',
            '__le__': 'bool'
        }[method_name]

        if return_type != expected_return_type:
            raise CompileError(f'{method_name}() must return {expected_return_type}',
                               node)

    def visit_FunctionDef(self, node):
        self.context.push()
        method_name = node.name
        return_type = self.return_type_string(node.returns)

        if node.decorator_list:
            raise Exception("methods must not be decorated")

        if len(node.args.args) == 0 or node.args.args[0].arg != 'self':
            raise CompileError('methods must take self as their first argument', node)

        params = params_string(method_name,
                               node.args.args[1:],
                               self.source_lines,
                               self.context)

        if method_name == '__init__':
            raise CompileError('__init__ is not allowed in a trait', node)
        elif method_name == '__del__':
            raise CompileError('__del__ is not allowed in a trait', node)
        elif method_name in METHOD_OPERATORS:
            self.validate_operator_signature(method_name,
                                             params,
                                             return_type,
                                             node)
            method_name = 'operator' + METHOD_OPERATORS[method_name]

        self.context.pop()

        return f'{return_type} {self._class_name}::{method_name}({params}) {{}}'

    def generic_visit(self, node):
        raise InternalError("unhandled node", node)

class BodyVisitor(BaseVisitor):
    pass

class AnnAssignVisitor(BaseVisitor):

    def visit_AnnAssign(self, node):
        target, mys_type, code = self.visit_ann_assign(node)
        self.context.define_global_variable(target, mys_type, node.target)

        return code

class ClassMemberValueVisitor(BaseVisitor):

    def visit_AnnAssign(self, node):
        return self.visit_ann_assign(node)[2]
