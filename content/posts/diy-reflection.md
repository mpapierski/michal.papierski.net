---
title: "DIY reflection"
date: 2018-04-08T15:31:25+02:00
draft: true
---

Whenever I'm writing a backend service in C++ there happen to be a problem with serialization of structures from/to a persistent store. Be it a database, network protocol, file, or anything. Basically anytime you're forced to write code such as:


{{< highlight cpp "linenos=table" >}}
// myPersistentStore is a connection to a database,
// and method below runs a SQL query.
myPersistentStore.query(R"SQL("SELECT "field1", "field2", "field3", ..., "field42" FROM "account")SQL");
// fetchAll returns a iterable view on database cursor,
// and row contains a map-like object where you can access value of a
// specific column by its name.
for (auto&& row : myPersistentStore.fetchAll()) {
  MyStructure myStructure;
  myStructure.field1 = row["field1"];
  myStructure.field2 = row["field2"];
  myStructure.field3 = std::stoi(row["field3"]);
  // ...
  myStructure.field42 = std::stoull(row["field42"]);
}
{{< / highlight >}}

If you have a fairly big database, with large amount of different fields it can be headache to extend anything -- lots of repetition.

There exists at least few ORMs for C++ which I can use right now, which sort of solves this problem for me in the way that I wouldn't write SQL by hand. What if I don't have database, but a binary file for instance. I need a solution that is flexible, and doesn't enforce a whole new paradigm.

I should tackle this problem from a different angle -- I need to list all the fields with their types and names. But -- you may wonder -- [https://wg21.link/P0578](reflection is still in proposal stage) and its not guaranteed to be part of C++20. How to do that?

For instance I can abuse preprocessor to enrich my `myStructure` with custom annotations.

{{< highlight cpp "linenos=table" >}}
struct Person: AutoProp<Person> {
  AUTOPROP_BEGIN(Person);

  std::string AUTOPROP(first_name);
  std::string AUTOPROP(last_name);
  
  int AUTOPROP(age);

  AUTOPROP_END();
};

Macro `AUTOPROP_BEGIN` shall generate a "prolog" of the class: an unique method that returns no attributes. Everytime `AUTOPROP` would be called it has to generate a new unique method, that would chain result of a method generated above it, with address and name of the property itself. At the end `AUTOPROP_END` shall generate a predictable method that calls the unique method generated above it which will predictably return a list of attributes in runtime.

Class `AutoProp<>` would expose additional methods such as `forEach` for enumerating. This base class would ingest those randomly generated methods through [https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern](CRTP).

Generated code will look similiar to:


{{< / highlight >}}
struct Person: AutoProp<Person> {
// Prolog
constexpr Empty getAttributes0() { return {}; }

std::string first_name;
constexpr auto getAttributes1() { return chain(getAttributes0(), makeAttribute(&Person::first_name, "first_name")); }
std::string last_name;
constexpr auto getAttributes2() { return chain(getAttributes1(), makeAttribute(&Person::last_name, "last_name")); }
int age;
constexpr auto getAttributes3() { return chain(getAttributes2(), makeAttribute(&Person::age, "age")); }

// Epilog
constexpr auto getAttributes() { return getAttributes3(); }
{{< / highlight >}}

