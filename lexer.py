import re

#TODO
# angka
# Variable identifier
# String literal

# CONSTANTS
TOKENS = {
    "=": "assignment",
    "+": "addition_sign",
    "-": "minus_sign",
    "*": "multiply",
    "/": "divide",
    ";": "semicolon",
    "$": "php_var",
    "function": "php_function",
    "class": "php_class",
    "echo": "php_print",
    "<?php": "php-opening-tag",
    "?>": "php-closing-tag",
    ".": "concat",
    "(": "open_bracket",
    ")": "closing_bracket",
    "{": "opening_curly_bracket",
    "}": "closing_curly_bracket",
    "#": "single-comment",
    "/*": "multi-line-comment",
    "*/": "multi-line-comment-closing",
    " ": "&nbsp"
}

# May or not may be used :P
class Token:
    def __init__(self, row_val, col_val, token_val):
        self.row = row_val
        self.col = col_val
        self.token = token_val
        self.value = None

    def __repr__(self):
        return f"{self.row},{self.col},{self.token},{self.value}"


# File reading
lines = []
with open("input1.php") as f:
    for line in f:
        lines.append(line.strip())

# Going through each line in the file
result_tokens = []
for row, line in enumerate(lines):
    # 5 + 2
    #     ^
    col = 0
    while (col < len(line)):
        if (line[col] in ".;(){}*-/+$="):
            result_tokens.append([row + 1, col + 1, TOKENS[line[col]]])
            col += 1
        elif ((col + len("<?php")) <= len(line)) and (line[col:col + len("<?php")] == "<?php"):
            result_tokens.append([row + 1, col + 1, TOKENS["<?php"]])
            col += len("<?php")
        elif (col + len("function") <= len(line)) and (line[col:col + len("function")] == "function"):
            result_tokens.append([row + 1, col + 1, TOKENS["function"]])
            # function name and etc (WIP)
        elif (col + len("class") <= len(line)) and (line[col: col + len("class")] == "class"):
            result_tokens.append([row + 1, col + 1, TOKENS["class"]])
        elif (col + len("echo") <= len(line)) and (line[col: col + len("echo")] == "echo"):
            result_tokens.append([row + 1, col + 1, TOKENS["echo"]])
        elif (col + len("?>") <= len(line)) and (line[col: col + len("?>")]) == "?>":
            result_tokens.append([row + 1, col + 1, TOKENS["?>"]])
            col += len("?>")


# Final output
def print_output():
    return
    # return "f{line_no},{column_no},{token_class}"

if __name__ == "__main__":
    print(result_tokens)