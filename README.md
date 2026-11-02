# Calculator

**Category:** Numbers

## Problem

A simple calculator to do basic operators. Make it a scientific calculator for added complexity.

## Solution

Parses expressions with `ast` and walks a strict whitelist of nodes: binary operators, unary signs, numeric constants, named constants (pi, e, tau) and a fixed set of math functions. No `eval()` is used, so arbitrary code cannot run. The REPL keeps the last result in `ans`.

## How to run

Requires Python 3.8+ and no third-party packages.

```bash
python3 main.py "2 + 3 * 4"
python3 main.py "sqrt(144) + sin(pi/2)"
python3 main.py            # interactive REPL
python3 main.py --demo
```

## Example

```text
2 + 3 * 4 = 14
           (2 + 3) * 4 = 20
               2 ** 10 = 1024
 sqrt(144) + sin(pi/2) = 13.0
        log(e) + 5 % 3 = 3.0
          -3 * (4 - 1) = -9
```

## Attribution

The problem statement is from [karan/Projects](https://github.com/karan/Projects), a list of practical projects that anyone can solve in any programming language (MIT License, Copyright (c) 2013 Karan Goel). The Python solution in this repository was implemented by [bspreston-esq](https://github.com/bspreston-esq).

This repository is part of the [Projects-Python-All](https://github.com/bspreston-esq/Projects-Python-All) collection.
