---
title: "Bootstrapping Rust from scratch"
date: 2019-02-21T12:09:41+01:00
draft: true
---

For past few years I've been following Rust project and every often I've tried to write something in it - but every time I was pushed back by the language complexity. Since recently I've tried to use it again and to my surprise all the language barriers were gone - it was actually pleasant to write code in it, and just in few days I felt really productive.

Rust project has gone through many design changes and quickly the main compiler gained the ability to be _self-hosted_ which means Rust compiler was rewritten in Rust. Since then if you want to build `rustc` from sources you have to use _stage0_ compiler which in current state is the previous _stable_ version. In the development cycle the train model is a bit more complicated[1].

When you want to build rust from the sources the process is easy and well documented and it hides all the complexity:

{{ <highlight sh>}}
git clone https://github.com/rust-lang/rust.git
cd rust
./x.py build && sudo ./x.py install
{{ </highlight> }}

But what if you want to do it yourself? And from scratch assuming you don't want to trust the provided binary compilers? How could you build Rust compiler from source when it wasn't written in Rust yet?

I got inspired by https://www.gnu.org/software/guix/blog/2018/bootstrapping-rust/. They actually found it easier to use `mrustc` (an alternative compiler) which assumes the Rust code is valid, and compiles it in a high-level assembly using C. This way they could start the bootstrap train with `1.19.0`.

I want to go deeper and go even earlier than that and make this process reproducible. 

Since early versions of Rust were written in Ocaml we should be fine with bootstraping the last Ocaml-written version of `rustc` and build our way up to the stable with that.

Lets start with https://github.com/rust-lang/rust/commit/ef75860a0a72f79f97216f8aaa5b388d98da6480.

# Building OCaml compiler

We need OCaml compiler and some other dependencies. Since I'm running quite modern Clang on my machine I also needed to patch some of the sources to disregard compiler errors.

{{ <highlight sh> }}
brew install ocaml opam
{{ </highlight>}}

`configure` mentions llvm-3.0, but doesn't compile cleanly against released 3.0 - we need to go deeper and find correct snapshot of it, and build it from sources. According to llvm history, and compile errors I tracked down the llvm snapshot to commit 097f9a94f66.



WIP.

Once OCaml `rustc` is built we can fight our way towards _stable_ channel.

[1]: https://github.com/rust-lang/rust/blob/1349c84a4fa0fca9b866b2e859d28ee185ca0c1b/src/stage0.txt#L5-L8