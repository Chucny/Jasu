import time
import requests

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
    return eval(expr)

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
def define_function(fname, *params, script=""):
    """
    Dynamically define a function in Jasu interpreter.

    fname : str -> function name
    *params : list of variable names (strings)
    script : str -> multiline python code as the function body
    """
    # Remove None parameters
    params = [p for p in params if p is not None]
    
    # Split script into lines
    block = script.strip().splitlines()
    
    # Register function in interpreter
    functions[fname] = (params, block)



def run_jasu(code):
    lines = code.splitlines()
    run_block(lines)

