import string


# CONSTANTS
TOKENS = {
    "=": "assign",
    "+": "addition_sign",
    "-": "minus_sign",
    "*": "math-times",
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
}


# Valid type-identifier checker
def get_variable(row, col, line, result_tokens, filename):
    length = 0
    while line[col + length] in (string.digits + string.ascii_letters + "_"):
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
    in_single_quote_string = False
    in_double_quote_string = False
    in_multiline_comment = False
    string_buffer = ""
    temp_row = -1
    temp_col = -1

    # Going through each line in the file
    for row, line in enumerate(lines):
        col = 0
        while col < len(line):
            # parsing multiline comments opening
            if (col + len("/*") <= len(line)) and (line[col:col + len("/*")] == "/*") and (not in_single_quote_string)\
                    and (not in_double_quote_string) and (not in_multiline_comment):
                temp_row = row
                temp_col = col
                in_multiline_comment = True
                col += 2

            # parsing multiline comments closing
            if (col + len("*/") <= len(line)) and (line[col:col + len("*/")] == "*/") and (not in_single_quote_string)\
                    and (not in_double_quote_string) and in_multiline_comment:
                in_multiline_comment = False
                col += 2

            if not in_multiline_comment:
                # parsing string literal single quote
                if (col < len(line)) and (line[col] == "\"") and (not in_single_quote_string):  # Checks if in single quote
                    if not in_double_quote_string:
                        temp_row = row
                        temp_col = col
                    string_buffer += "\""
                    col += 1
                    in_double_quote_string = not in_double_quote_string # If yes, disable double quote checking
                    if not in_double_quote_string:
                        result_tokens.append([temp_row + 1, temp_col + 1, "string-literal", string_buffer.replace(" ", "&nbsp")])
                        string_buffer = ""

                # parsing string literal double quote
                if (col < len(line)) and (line[col] == "\'") and (not in_double_quote_string):  # Checks if in double quote
                    if not in_single_quote_string:
                        temp_row = row
                        temp_col = col
                    string_buffer += "\'"
                    col += 1
                    in_single_quote_string = not in_single_quote_string # If yes, disable single quote checking
                    if not in_single_quote_string:
                        result_tokens.append([temp_row + 1, temp_col + 1, "string-literal", string_buffer.replace(" ", "&nbsp")])
                        string_buffer = ""

                if col >= len(line):
                    break

                if (col < len(line)) and (in_single_quote_string or in_double_quote_string):
                    if col + len("\\'") <= len(line) and (line[col:col + len("\\'")] == "\\'"):
                        string_buffer += "\\'"
                        col += 2
                        pass
                    elif col + len('\\"') <= len(line) and (line[col:col + len('\\"')] == '\\"'):
                        string_buffer += '\\"'
                        col += 2

                        # add more escape sequences
                    elif line[col] in "'\"":
                        string_buffer += "\\" + line[col]
                        col += 1
                    else:
                        string_buffer += line[col]
                        col += 1

                # parsing single line comments
                elif ((col + len("//")) <= len(line)) and (line[col:col + len("//")] == "//"):
                    break

                # (#) single line comments
                elif (col < len(line)) and (line[col] == "#"):
                    break

                # taking in single character tokens
                elif (col < len(line)) and (line[col] in ".;(){}*-/+="):
                    result_tokens.append([row + 1, col + 1, TOKENS[line[col]]])
                    col += 1

                # ignoring whitespace
                elif (col < len(line)) and (line[col] in string.whitespace):
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
                elif (col < len(line)) and (line[col] in "0123456789"):
                    length = 0
                    while line[col + length] in "0123456789":
                        length += 1
                    result_tokens.append([row + 1, col + 1, "number", int(line[col: col + length])])
                    col += length

                # parsing variable & identifiers
                elif (col < len(line)) and (line[col] == '$'):
                    result_tokens.append([row + 1, col + 1, TOKENS['$']])
                    col += 1
                    col += get_variable(row, col, line, result_tokens, filename)

                # unidentifiable token exception
                else:
                    raise Exception(f"{filename}:{row + 1}:{col + 1}:INVALID TOKEN FOUND")
            else:
                col += 1

    if in_double_quote_string or in_single_quote_string:
        raise Exception(f"{filename}:{temp_row + 1}:{temp_col + 1}:STRING IS NOT PROPERLY TERMINATED")

    if in_multiline_comment:
        raise Exception(f"{filename}:{temp_row + 1}:{temp_col + 1}:MULTILINE COMMENT IS NOT PROPERLY TERMINATED")

    return result_tokens


# Final output
def print_output(result: list):
    for line in result:
        if len(line) == 3:    # If line doesn't have value
            row, col, name = line
            print(f"{row},{col},{name}")
        elif len(line) == 4:  # If line does have value
            row, col, name, val = line
            print(f"{row},{col},{name},{val}")


def main():
    filename = input("Enter the PHP filename: ")
    if filename.endswith(".php"):
        result_tokens = token_lexer(filename)
        print_output(result_tokens)
    else:
        print("Not a valid PHP source code filename!")


if __name__ == "__main__":
    main()
