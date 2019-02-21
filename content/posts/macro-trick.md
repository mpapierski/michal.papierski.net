+++
title = "Macro trick"
date = "2016-11-18T16:06:33+01:00"
tags = [ "Development", "c++" ]
categories = [ "Development" ]

+++

Sometimes you need to create some enum, and for each of the values you want
to assign some additional information -- a string. Imagine a
lookup function that based on some constant returns a description of the
provided value.

Nothing special -- first thing that comes to your mind might be a global
instance of `std::map`, right?

{{< highlight cpp "linenos=table" >}}
enum Color { Red, Green, Blue };

std::map<Color, std::string> kColors{
    {Red, "#ff0000"}, {Green, "#00ff00"}, {Blue, "#0000ff"}};

std::string HTML(const Color color) { return kColors[color]; }

{{< / highlight >}}

We have constants for colors, we store HTML values for each of the color
constant and when there is a need to check its html value we just do a
lookup. Simple as that. However there are two major things that are wrong
with this code:

1. `std::map` has `O(log N)` lookup times
2. `std::string` sounds unnecessary because we do not plan to modify the lookup
    table

Lookup function might hurt, and `std::string` seems overkill.

While we can use `std::unordered_map` which might improve our lookup times to
`O(1)` on average, there is better solution:

{{< highlight cpp "linenos=table" >}}
enum Color { Red, Green, Blue };

const char *HTML(const Color color) {
  switch (color) {
  case Red:
    return "#ff0000";
  case Green:
    return "#00ff00";
  case Blue:
    return "#0000ff";
  default:
    return nullptr;
  }
}
{{< / highlight >}}

Compilers are smart enough to output a lookup table for our `switch`
statement. This gives us a `O(1)` constant lookup time which is a nice
improvement over original `O(log N)`.

There is still another problem with this solution though.

_Code duplication_. Every time you plan to add new value to your enum you have
to update the switch statement too manually -- and manual process is almost
always source of mistakes and it requires an _action_. How to solve this problem
and maintain a constant `O(1)` lookup times?

_Preprocessor macro._

{{< highlight cpp "linenos=table" >}}
#define ENUM_COLORS(XX) \
  XX(Red, "#ff0000")    \
  XX(Green, "#00ff00")  \
  XX(Blue, "#0000ff")

enum Color {
#define XX(name, value) name,
  ENUM_COLORS(XX)
#undef XX
      Unknown
};

const char *HTML(const Color color) {
  switch (color) {
#define XX(name, value) \
  case name:            \
    return value;
    ENUM_COLORS(XX)
#undef XX
  default:
    return nullptr;
  }
}

int main() {
  std::cout << HTML(Red) << '\n';
  std::cout << HTML(Green) << '\n';
  std::cout << HTML(Blue) << '\n';
};
{{< / highlight >}}

Now adding new color is just adding new line to the `ENUM_COLORS` macro.

What about function that returns *actual* name of the
color?

{{< highlight cpp "linenos=table" >}}
const char *Name(const Color color) {
  switch (color) {
#define XX(name, value) \
  case name:            \
    return #name;
    ENUM_COLORS(XX)
#undef XX
  default:
    return nullptr;
  }
}
{{< / highlight >}}

Lets explore this idea further. Lets say we want to list all the colors
we have in our enum. First we need a code to
populate a list which values we know.

{{< highlight cpp "linenos=table" >}}
constexpr struct {
  const char *name;
  const char *value;
} kColors[] = {
#define XX(name, value) { #name, value },
ENUM_COLORS(XX)
#undef XX
  {nullptr, nullptr}
};
{{< / highlight >}}

And actual code for listing all the colors and values:

{{< highlight cpp "linenos=table" >}}
for (auto *it = kColors; it->name != nullptr; ++it) {
  std::cout << it->name << "=" << it->value << '\n';
}
{{< / highlight >}}
