#include "mys.hpp"

std::shared_ptr<List<String>> create_args(int argc, const char *argv[])
{
    int i;
    auto args = std::make_shared<List<String>>();

    for (i = 0; i < argc; i++) {
        args->append(argv[i]);
    }

    return args;
}

std::ostream&
operator<<(std::ostream& os, const Exception& e)
{
    os << e.what();

    return os;
}

std::ostream&
operator<<(std::ostream& os, const std::exception& e)
{
    os << e.what();

    return os;
}

std::ostream&
operator<<(std::ostream& os, const String& obj)
{
    if (obj.m_string) {
        os << *obj.m_string;
    } else {
        os << "None";
    }

    return os;
}

#if defined(MYS_TEST)

#define ANSI_COLOR_RED "\x1b[31m"
#define ANSI_COLOR_GREEN "\x1b[32m"
#define ANSI_COLOR_YELLOW "\x1b[33m"
#define ANSI_COLOR_BLUE "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN "\x1b[36m"

#define ANSI_BOLD "\x1b[1m"
#define ANSI_RESET "\x1b[0m"

#define COLOR(color, ...) ANSI_RESET ANSI_COLOR_##color __VA_ARGS__ ANSI_RESET

#define BOLD(...) ANSI_RESET ANSI_BOLD __VA_ARGS__ ANSI_RESET

#define COLOR_BOLD(color, ...)                                          \
    ANSI_RESET ANSI_COLOR_##color ANSI_BOLD __VA_ARGS__ ANSI_RESET

Test *tests_head_p = NULL;
Test *tests_tail_p = NULL;

#include <chrono>

using namespace std::chrono;

int main()
{
    Test *test_p;
    int passed = 0;
    int failed = 0;
    int total = 0;
    const char *result_p;

    test_p = tests_head_p;

    while (test_p != NULL) {
        auto begin = steady_clock::now();

        try {
            test_p->m_func();
            result_p = COLOR(GREEN, " ✔");
            passed++;
        } catch (std::exception &e) {
            std::cout << "Message: " << e << std::endl;
            result_p = COLOR(RED, " ✘");
            failed++;
        }

        auto end = steady_clock::now();
        auto duration = duration_cast<milliseconds>(end - begin).count();

        std::cout
            << result_p
            << " " << test_p->m_name_p
            << " (" <<  duration << " ms)"
            << std::endl;

        total++;
        test_p = test_p->m_next_p;
    }

    if (failed == 0) {
        return (0);
    } else {
        return (1);
    }
}

#elif defined(MYS_APPLICATION)

extern void package_main(int argc, const char *argv[]);

int main(int argc, const char *argv[])
{
    int res;

    try {
        package_main(argc, argv);
        res = 0;
    } catch (std::exception &e) {
        std::cerr << e << std::endl;
        res = 1;
    }

    return (res);
}

#endif

std::ostream& operator<<(std::ostream& os, const Bool& obj)
{
    if (obj.m_value) {
        os << "True";
    } else {
        os << "False";
    }

    return os;
}

std::ostream& operator<<(std::ostream& os, const Char& obj)
{
    // ToDo...
    os << (char)obj.m_value;

    return os;
}

const String& string_not_none(const String& obj)
{
    if (!obj.m_string) {
        throw AttributeError("object is None");
    }

    return obj;
}

std::ostream& operator<<(std::ostream& os, const Object& obj)
{
    obj.__format__(os);

    return os;
}
