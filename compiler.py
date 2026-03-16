import time
import requests
import math
import random
# jasu programming language


variables = {}
functions = {}

# Exceptions for return and break
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

def eval_expr(expr):
    expr = expr.strip()
    # Replace variables safely
    for name, value in variables.items():
        expr = expr.replace(name, repr(value))
    return eval(expr, {"__builtins__": None}, python_functions | variables)

def run_block(lines):
    i = 0
    last_if_result = False
    while i < len(lines):
        line = lines[i].strip()

        # return
        if line.startswith("#return("):
            content = line[8:-2]
            raise ReturnException(eval_expr(content))

        # break
        elif line.startswith("#break()"):
            raise BreakException()

        # var
        elif line.startswith("var "):
            line = line[4:].replace(";", "")
            name, value = line.split(" = ", 1)

            if value.startswith("read("):
                prompt = value[5:-2].strip('"')
                variables[name] = input(prompt)
            elif value.startswith("fetch("):
                args = value[6:-1].split(",")
                url = eval_expr(args[0].strip())
                method = "GET"
                if len(args) > 1:
                    method = args[1].strip('"').upper()
                if method == "GET":
                    variables[name] = requests.get(url).text
                elif method == "POST":
                    variables[name] = requests.post(url).text
                else:
                    variables[name] = f"Unsupported method {method}"
            else:
                variables[name] = eval_expr(value)

        # write
        elif line.startswith("write("):
            content = line[6:-2]
            if content in variables:
                print(variables[content])
            else:
                print(eval_expr(content))

        # wait
        elif line.startswith("wait("):
            seconds = line[5:-2]
            time.sleep(float(eval_expr(seconds)))

        # replace
        elif ".replace(" in line:
            varname, rest = line.split(".replace(")
            args = rest[:-2].split(", ")
            old = args[0].strip('"')
            new = args[1].strip('"')
            variables[varname] = variables[varname].replace(old, new)

        # if
        elif line.startswith("if("):
            condition = line[3:].split("){")[0]
            block = []
            i += 1
            while lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            last_if_result = eval_expr(condition)
            if last_if_result:
                run_block(block)

        # elif
        elif line.startswith("elif("):
            if last_if_result:  # skip block if previous if ran
                i += 1
                while lines[i].strip() != "}":
                    i += 1
            else:
                condition = line[5:].split("){")[0]
                block = []
                i += 1
                while lines[i].strip() != "}":
                    block.append(lines[i])
                    i += 1
                last_if_result = eval_expr(condition)
                if last_if_result:
                    run_block(block)

        # else
        elif line.startswith("else{"):
            block = []
            i += 1
            while lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            if not last_if_result:
                run_block(block)

        # function define
        elif line.startswith("define["):
            header = line[7:].split("]{")[0]
            fname = header.split("(")[0]
            params = header.split("(")[1][:-1].split(",")
            block = []
            i += 1
            while lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            functions[fname] = (params, block)

        # function call
        elif "(" in line and line.endswith(");"):
            fname = line.split("(")[0]
            if fname in functions:
                args = line.split("(")[1][:-2].split(",")
                params, block = functions[fname]
                backup = variables.copy()
                for p, a in zip(params, args):
                    variables[p.strip()] = eval_expr(a.strip())
                try:
                    run_block(block)
                except ReturnException as e:
                    variables.clear()
                    variables.update(backup)
                    variables["_last_return"] = e.value
                variables.clear()
                variables.update(backup)

        # while loop
        elif line.startswith("while("):
            condition = line[6:].split("){")[0]
            block = []
            i += 1
            while lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            try:
                while eval_expr(condition):
                    try:
                        run_block(block)
                    except BreakException:
                        break
            except Exception as e:
                print("Error in while loop:", e)

        i += 1

def run_jasu(code):
    lines = code.splitlines()
    run_block(lines)

import time
import requests
from colorama import Fore, Style, init

init(autoreset=True)  # automatically reset colors

variables = {}
functions = {}

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

# map color names
colors = {
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "none": ""
}

def eval_expr(expr):
    expr = expr.strip()
    for name, value in variables.items():
        expr = expr.replace(name, repr(value))
    try:
        return eval(expr)
    except:
        return expr  # if cannot eval (like string), return as is

def run_block(lines):
    i = 0
    last_if_result = False
    while i < len(lines):
        line = lines[i].strip()

        # return
        if line.startswith("#return("):
            content = line[8:-2]
            raise ReturnException(eval_expr(content))

        # break
        elif line.startswith("#break()"):
            raise BreakException()

        # var
        elif line.startswith("var "):
            line = line[4:].replace(";", "")
            name, value = line.split(" = ", 1)

            # read()
            if value.startswith("read("):
                prompt = value[5:-2].strip('"')
                variables[name] = input(prompt)
            # fetch()
            elif value.startswith("fetch("):
                args = value[6:-1].split(",")
                url = eval_expr(args[0].strip())
                method = "GET"
                if len(args) > 1:
                    method = args[1].strip('"').upper()
                if method == "GET":
                    variables[name] = requests.get(url).text
                elif method == "POST":
                    variables[name] = requests.post(url).text
                else:
                    variables[name] = f"Unsupported method {method}"
            else:
                variables[name] = eval_expr(value)

        # write with optional color
        elif line.startswith("write("):
            inner = line[6:-1]
            if "," in inner:  # check for color
                content_part, color_part = inner.split(",", 1)
                content = eval_expr(content_part.strip())
                color_name = color_part.strip().split("=")[-1]
                color_code = colors.get(color_name.lower(), "")
            else:
                content = eval_expr(inner.strip())
                color_code = ""
            print(f"{color_code}{content}{Style.RESET_ALL}")

        # wait
        elif line.startswith("wait("):
            seconds = line[5:-2]
            time.sleep(float(eval_expr(seconds)))

        # replace
        elif ".replace(" in line:
            varname, rest = line.split(".replace(")
            args = rest[:-2].split(", ")
            old = args[0].strip('"')
            new = args[1].strip('"')
            variables[varname] = variables[varname].replace(old, new)

        # if
        elif line.startswith("if("):
            condition = line[3:].split("){")[0]
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            last_if_result = eval_expr(condition)
            if last_if_result:
                run_block(block)

        # elif
        elif line.startswith("elif("):
            if last_if_result:  # skip block if previous if ran
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    i += 1
            else:
                condition = line[5:].split("){")[0]
                block = []
                i += 1
                while i < len(lines) and lines[i].strip() != "}":
                    block.append(lines[i])
                    i += 1
                last_if_result = eval_expr(condition)
                if last_if_result:
                    run_block(block)

        # else
        elif line.startswith("else{"):
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            if not last_if_result:
                run_block(block)

        # function define
        elif line.startswith("define["):
            header = line[7:].split("]{")[0]
            fname = header.split("(")[0]
            params = header.split("(")[1][:-1].split(",")
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            functions[fname] = (params, block)

        # function call
        elif "(" in line and line.endswith(");"):
            fname = line.split("(")[0]
            if fname in functions:
                args = line.split("(")[1][:-2].split(",")
                params, block = functions[fname]
                backup = variables.copy()
                for p, a in zip(params, args):
                    variables[p.strip()] = eval_expr(a.strip())
                try:
                    run_block(block)
                except ReturnException as e:
                    variables.clear()
                    variables.update(backup)
                    variables["_last_return"] = e.value
                variables.clear()
                variables.update(backup)

        # while loop
        elif line.startswith("while("):
            condition = line[6:].split("){")[0]
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "}":
                block.append(lines[i])
                i += 1
            try:
                while eval_expr(condition):
                    try:
                        run_block(block)
                    except BreakException:
                        break
            except Exception as e:
                print("Error in while loop:", e)

        i += 1
python_functions = {}

def define_function(fname, *params, script=""):
    params = [p for p in params if p is not None]

    def pyfunc(*args):
        local_vars = dict(zip(params, args))

        code = script.strip().split(";")
        result = None

        for line in code:
            line = line.strip()
            if not line:
                continue

            if line.startswith("return"):
                expr = line[6:].strip("() ")
                result = eval(expr, globals(), local_vars)
                return result
            else:
                exec(line, globals(), local_vars)

        return result

    python_functions[fname] = pyfunc






define_function("sin", "a", script="return(math.sin(a))")
define_function("cos", "a", script="return(math.cos(a))")
define_function("tan", "a", script="return(math.tan(a))")

define_function("sqrt", "a", script="return(math.sqrt(a))")
define_function("log", "a", script="return(math.log(a))")

define_function("floor", "a", script="return(math.floor(a))")
define_function("ceil", "a", script="return(math.ceil(a))")

define_function("abs", "a", script="return(abs(a))")
define_function("round", "a", script="return(round(a))")

define_function("max", "a", "b", script="return(max(a,b))")
define_function("min", "a", "b", script="return(min(a,b))")

define_function("randint", "a", "b", script="return(random.randint(a,b))")
define_function("random", script="return(random.random())")
define_function("choice", "a", script="return(random.choice(a))")

define_function("len", "a", script="return(len(a))")

define_function("int", "a", script="return(int(a))")
define_function("float", "a", script="return(float(a))")
define_function("str", "a", script="return(str(a))")

define_function("time", script="return(time.time())")

define_function("pi", script="return(math.pi)")





def run_jasu(code):
    lines = code.splitlines()
    run_block(lines)


import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compiler.py file.jasu")
    else:
        filename = sys.argv[1]

        if filename.endswith(".jasu"):
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()

            run_jasu(code)
        else:
            print("Only .jasu files supported")



input()
