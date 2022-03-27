import re, string

# TODO
# String literal
# single line comment (if read)
# multi line comment (if read)

# CONSTANTS
TOKENS = {
    "=": "assign",
    "+": "addition_sign",
    "-": "minus_sign",
    "*": "multiply",
    "/": "divide",
    ";": "semicolon",
    "$": "variable",
    "function": "function",
    "class": "class",
    "echo": "print-output",
    "<?php": "php-opening-tag",
    "?>": "php-closing-tag",
    ".": "concate",
    "(": "bracket-opening",
    ")": "bracket-closing",
    "{": "curly-bracket-opening",
    "}": "curly-bracket-closing",
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


def get_variable(row, col, line, result_tokens, filename):
    length = 0
    while (line[col + length] in (string.digits + string.ascii_letters + "_")):
        if (length == 1) and (line[col + length] in string.digits):
            raise Exception(f"{filename}:{row + 1}:{col + length + 1}:VARIABLE NAME CANNOT START WITH DIGIT")
        else:
            length += 1
    result_tokens.append([row + 1, col + 1, "type-identifier", line[col:col + length]])
    return length


def token_lexer(filename: str) -> list:
    lines = []
    with open(filename) as f:
        for line in f:
            lines.append(line)

    result_tokens = []
    # Going through each line in the file
    for row, line in enumerate(lines):
        col = 0
        while (col < len(line)):
            # parsing single line comments
            if ((col + len("//")) <= len(line)) and (line[col:col + len("//")] == "//"):
                # TODO: Implement logic
                break

            # taking in single character tokens
            elif (line[col] in ".;(){}*-/+="):
                result_tokens.append([row + 1, col + 1, TOKENS[line[col]]])
                col += 1

            # ignoring whitespace
            elif (line[col] in string.whitespace):
                col += 1

            # parsing opening php tag
            elif ((col + len("<?php")) <= len(line)) and (line[col:col + len("<?php")] == "<?php"):
                result_tokens.append([row + 1, col + 1, TOKENS["<?php"]])
                col += len("<?php")

            # parsing function keyword
            elif (col + len("function") <= len(line)) and (line[col:col + len("function")] == "function"):
                result_tokens.append([row + 1, col + 1, TOKENS["function"]])
                col += len("function") + 1
                col += get_variable(row, col, line, result_tokens, filename)

            # NEED TO TEST
            # parsing class keyword
            elif (col + len("class") <= len(line)) and (line[col: col + len("class")] == "class"):
                result_tokens.append([row + 1, col + 1, TOKENS["class"]])
                col += len("class") + 1 # add the extra space
                col += get_variable(row, col, line, result_tokens, filename)

            # parsing echo keyword
            elif (col + len("echo") <= len(line)) and (line[col: col + len("echo")] == "echo"):
                result_tokens.append([row + 1, col + 1, TOKENS["echo"]])
                col += len("echo")

            # parsing closing php tag
            elif (col + len("?>") <= len(line)) and (line[col: col + len("?>")]) == "?>":
                result_tokens.append([row + 1, col + 1, TOKENS["?>"]])
                col += len("?>")

            # parsing integers not decimals
            elif (line[col] in "0123456789"):
                length = 0
                while (line[col + length] in "0123456789"):
                    length += 1
                result_tokens.append([row + 1, col + 1, "number", int(line[col: col + length])])
                col += length

            # parsing variable & identifiers
            elif line[col] == '$':
                result_tokens.append([row + 1, col + 1, TOKENS['$']])
                col += 1
                col += get_variable(row, col, line, result_tokens, filename)

            # unidentifiable token exception
            else:
                raise Exception(f"{filename}:{row + 1}:{col + 1}:INVALID TOKEN FOUND")

    return result_tokens


# Final output
def print_output(result: list) -> str:
    for line in result:
        print(str(line).replace("'", "").replace(" ", "").strip("[]"))


def main():
    filename = input("Enter the PHP filename: ")
    if filename.endswith(".php"):
        result_tokens = token_lexer(filename)
        print_output(result_tokens)
    else:
        print("Not a valid PHP source code filename!")


if __name__ == "__main__":
    main()
