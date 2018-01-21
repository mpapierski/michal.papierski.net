+++
date = "2017-04-04T17:53:07+02:00"
categories = []
keywords = []
description = ""
title = "Introduction to CMake"
draft = true
+++

CMake is a build system that works. Actually this is not a build system. This is a "meta" build system because it generates a build system out of a `CMakeLists.txt` definition and actual building happens using that tool. It basically means that we can use it to generate `Makefile` and build our project using `make` command. Of course we are not limited to `make`! From the same `CMakeLists.txt` file we can also generate `Visual Studio Solution`, or any other supported tool. This will solve your problems when you have to support two platforms: one for automake, and `.sln` for Visual Studio. Before you had support two separate build systems and after switching you can throw away those files and just stick to `cmake`.

Speaking of portability we have all major platforms supported: Linux, macOS and Windows. According to docs there are more platforms and architectures supported. Each of those platforms contains different generators so I believe `cmake` will serve all your portability needs.

This is, of course, open source tool using BSD license. Behind this tool is `Kitware` company which develops it, and also they use it in their products. And there is a huge community. They started it in 1999 because they needed a tool that will help them support multiple platforms. Since there were no alternatives they started their own.

CMake has its own scripting language to describe build rules. In comparision to other similiar tools this is a declarative language. You will describe your build process using simple commands. You can blame it for another language but personally I do not see it as a flaw.

# How to use CMake?

First of all there is a command that you will use the most. This will take your `CMakeLists.txt` and will output a `Makefile`.

```sh
cmake -G Generator -DVARIABLE1 -DVARIABLE2 ~/Project
```

You can pass variables to your script using `-D` switches. There might be some confusion - this is not a flag for your compiler. This is just just for your build script so you can have feature switches and other good things.

This is called _configuration_ step - a step where `cmake` takes all your commands, finds all dependencies you want, and outputs a project usign a generator.

After successful run CMake will also output a cache to remember what happened during this step. You are supposed to never touch this file. After every change of your build script this file will be generated again.

Now you can build your project:

```sh
make
```

This is _build_ step. In this case we have all specified rules materialized into a `Makefile` which we can use to build our stuff. Again, you are supposed to never touch this file. After every change to your build scripts that file will be generated again.

What if you need to build `Visual Studio`, or `Xcode` project? And you need to support Linux as well? No need to remember all those command lines for different generators to trigger builds. There is another command line switch in cmake that will build your project regardless of your generator. Think of it as a wrapper for your IDE.

```sh
cmake \
  --build \
  --target target \
  --config Release \
  --clean-first \
  --use-stderr \
  A_directory_where_you_generated_your_project
```

All those command line switches might be confusing to you so here is little explanation without going too deep into details.

* `--build` is the command line switch that makes it a wrapper for your tool (`make`, `Visual Studio`, `Xcode` or whatever you use).
* `--target` - optional. But you can tell it to build just specific target you want.
* `--config` - optional.Some generators supports multiple configurations (i.e. `Visual Studio`, `Xcode`), others not (i.e. `Unix Makefiles`)
* `--clean-first` - This will clean your build outputs before doing actual build.
* `--use-stderr` - This will use actually use `stderr` if the native build tool writes anything to `stderr` too. Otherwise everything will be in `stdout` of the process.
* And last argument is a directory where you called cmake to generate your project first.

If you are afraid of command line there are graphical tools to help you in using your project such as `cmake-gui` which is installed by default on Windows.

I assume you have at least basic knowledge about building software. Before going into deep waters with you I want to ask first what is a a compilation process?

```
source -> executable
```

_maybe a nice diagram here will do_

Going deeper, in C++ this roughly means:

1. Preprocessing

  `input.cpp + input.h + iostream -> source.cpp`

   In simpler words it means that your source is processed into translation units.

2. Compilation

  `input.cpp -> input.o`

3. Linking

  `foo.o bar.o -> a.out`

Those three stages are nothing more than invocation on commands. So going deeper:

1. Preprocess

  `g++ -E input.cpp -o source.cpp` - This is done for us by compiler already. No need to think about it.

2. Compilation

  `g++ -c source.cpp -o source.o`

3. Linking

  `g++ source.o -o output` 

There is a pattern. There is input, and output. Output of one command could be an input to different command.

# Overview

Your script is made of commands. Command names are case-insensitive.

```cmake
cmake_minimum_required(VERSION 3.0)
project(my_project)
```

Arguments could be quoted, or escaped. In case you need longer, multi line arguments there are also bracket arguments[^1].

```cmake
# Quoted
project("my_project")
# Normal
add_executable(my_project main.cpp)
# Bracket
message(STATUS [=[
This
is
a
bracket
with unique marker which is
equal sign
]=])
```

Variable references has the form `${variable}`. Whether you will put it inside quoted or unquoted argument does not make difference. Such reference is expanded and replaced with the contents of variable. You can also reference environment variables the same which is slightly different form: `$ENV{VAR}`.

Comments starts with `#`.

## Control structures

As it is scripting language there are constructions to control flow of your script. 

### Conditional blocks

You can control flow of your script with conditional statements:

```cmake
if(var1)
message("foo")
elif(var2)
message("bar")
else()
message("baz")
endif()
```

### Loops

TBD

### Command definitions

TBD

## Variables

TBD

### Useful variables

* `CMAKE_CURRENT_SOURCE_DIR`
* `CMAKE_CURRENT_BINARY_DIR`

# Tutorial

This is the place where you will learn how to write build scripts and how to do it properly.

## Boilerplate

Every script starts with some boilerplate.

```cmake
cmake_minimum_required (VERSION 3.0)
project (my_project)
```

TBD

[^1]: This is available since version 3.0
