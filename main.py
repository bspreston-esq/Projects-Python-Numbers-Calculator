#!/usr/bin/env python3
"""A safe scientific calculator: expressions are parsed, never eval()'d."""
import argparse
import ast
import math
import operator

BIN_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod, ast.Pow: operator.pow,
}
UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}

FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sqrt": math.sqrt, "log": math.log, "ln": math.log, "log10": math.log10,
    "exp": math.exp, "floor": math.floor, "ceil": math.ceil,
    "fabs": math.fabs, "degrees": math.degrees, "radians": math.radians,
}
CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}

class CalculatorError(Exception):
    pass

def evaluate(expression: str, variables=None):
    """Evaluate an arithmetic/scientific expression safely."""
    variables = dict(variables or {})
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise CalculatorError(f"syntax error: {exc.msg}") from exc

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise CalculatorError("only numbers are allowed")
        if isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            if node.id in CONSTANTS:
                return CONSTANTS[node.id]
            raise CalculatorError(f"unknown name '{node.id}'")
        if isinstance(node, ast.BinOp) and type(node.op) in BIN_OPS:
            left, right = walk(node.left), walk(node.right)
            try:
                return BIN_OPS[type(node.op)](left, right)
            except ZeroDivisionError:
                raise CalculatorError("division by zero")
            except OverflowError:
                raise CalculatorError("result too large")
        if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPS:
            return UNARY_OPS[type(node.op)](walk(node.operand))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id not in FUNCTIONS:
                raise CalculatorError(f"unknown function '{node.func.id}'")
            if node.keywords:
                raise CalculatorError("keyword arguments are not supported")
            return FUNCTIONS[node.func.id](*[walk(a) for a in node.args])
        raise CalculatorError(f"unsupported syntax: {type(node).__name__}")

    result = walk(tree)
    if isinstance(result, complex):
        raise CalculatorError("result is not a real number")
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expression", nargs="?")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    if args.demo:
        for expr in ("2 + 3 * 4", "(2 + 3) * 4", "2 ** 10", "sqrt(144) + sin(pi/2)",
                     "log(e) + 5 % 3", "-3 * (4 - 1)"):
            print(f"{expr:>24} = {evaluate(expr)}")
        return

    if args.expression:
        try:
            print(evaluate(args.expression))
        except CalculatorError as exc:
            print(f"Error: {exc}")
        return

    print("Scientific calculator. Functions: " + ", ".join(sorted(FUNCTIONS)))
    print("Constants: pi, e, tau. Type 'quit' to exit.")
    variables = {}
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if line.lower() in {"quit", "exit"}:
            break
        if not line:
            continue
        try:
            value = evaluate(line, variables)
            variables["ans"] = value
            print(value)
        except (CalculatorError, ValueError, TypeError) as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
