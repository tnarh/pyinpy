import os
import traceback
import inspect
import stat
from datetime import datetime
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pygments.styles import get_style_by_name

code = []

def clear():
    os.system("clear")

def highlight_code(code_str):
    style = get_style_by_name('monokai')
    return highlight(code_str, PythonLexer(), TerminalFormatter(style=style))

while True:
    clear()
    for i, (line, indent) in enumerate(code):
        colored_line = highlight_code(line.rstrip('\n'))
        print(f"{i+1} | {' ' * indent}{colored_line}", end='')

    line = input(f"{len(code)+1} | ")

    if line == ':prev':
        if len(code) > 0:
            code.pop()  # Remove the current line
    elif line == ':execute':
        clear()
        code_str = "\n".join([line for line, _ in code])
        try:
            exec(code_str)
        except Exception as e:
            print(f"!!!!!!!!!!!!!!!!!!!!!!!! Error in line {i+1}:")
            traceback.print_exc()
        input("[press enter to continue]")
    elif line.startswith(':save '):
        name = line.split(" ")[1]
        with open(f'documents/{name}', 'w') as file:
            file.write("")
        with open(f'documents/{name}', 'a') as file:
            for code_line, _ in code:
                file.write(f'{code_line}\n')
    elif line.startswith(':open '):
        name = line.split(" ")[1]
        with open(f'documents/{name}', 'r') as file:
            code = [(line.strip(), len(line) - len(line.lstrip())) for line in file.readlines()]
    elif line == ':my':
        directory_path = 'documents/'

        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        for file in files:
            file_path = os.path.join(directory_path, file)
            file_stat = os.stat(file_path)

            # Extract information from the file_stat
            mode = stat.filemode(file_stat.st_mode)
            size = file_stat.st_size
            modification_time = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            # Print the information
            print(f"{mode} {size} bytes {modification_time} {file}")
        input("[press enter to continue]")
    elif line == ':exit':
        print("Thank you for using python_runner")
        break
    else:
        indent = len(line) - len(line.lstrip())
        code.append((line, indent))

