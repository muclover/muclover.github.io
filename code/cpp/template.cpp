#include <cassert>
#include <iostream>

namespace jc
{

    template <typename T, typename U>
    auto max(const T &a, const U &b) -> decltype(true ? a : b)
    {
        return a < b ? b : a;
    }

} // namespace jc

int main()
{

    assert(jc::max(1.8, 0.14) == 3.14);
    int a = 1;
    double b = 3.1;
    decltype(true ? a : b) c;
}