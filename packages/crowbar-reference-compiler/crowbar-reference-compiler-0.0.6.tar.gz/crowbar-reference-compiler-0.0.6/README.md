the reference compiler for the [Crowbar](https://sr.ht/~boringcactus/crowbar-lang/) language.

requirements:
* [QBE](https://c9x.me/compile/) installed somewhere on your PATH
* gcc

usage (i probably will forget to update this so [check directly](https://git.sr.ht/~boringcactus/crowbar-reference-compiler/tree/main/crowbar_reference_compiler/__init__.py)):
```
usage: crowbarc-reference [-h] [-V] [-g] [--stop-at-parse-tree]
                          [--stop-at-qbe-ssa] [-S] [-c] [-D DEFINE_CONSTANT]
                          [-I INCLUDE_DIR] [-o OUT]
                          input

The reference compiler for the Crowbar programming language

positional arguments:
  input                 input file

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -g, --include-debug-info
  --stop-at-parse-tree
  --stop-at-qbe-ssa
  -S, --stop-at-assembly
  -c, --stop-at-object
  -D DEFINE_CONSTANT, --define-constant DEFINE_CONSTANT
                        define a constant with some literal value
  -I INCLUDE_DIR, --include-dir INCLUDE_DIR
                        folder to look for included headers within
  -o OUT, --out OUT     output file
```
