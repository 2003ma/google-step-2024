#! /usr/bin/python3


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == ".":
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {"type": "NUMBER", "number": number}
    return token, index


def read_plus(line, index):
    token = {"type": "PLUS"}
    return token, index + 1


def read_minus(line, index):
    token = {"type": "MINUS"}
    return token, index + 1


def read_mul(line, index):
    token = {"type": "MUL"}
    return token, index + 1


def read_divide(line, index):
    token = {"type": "DIVIDE"}
    return token, index + 1


# 括弧を読む
def read_parentheses(line, index):
    if line[index] == "(":
        token = {"type": "PARENTHESES", "PAIR": "("}
    else:
        token = {"type": "PARENTHESES", "PAIR": ")"}
    return token, index + 1


def calculate_mul(num1, num2):
    return num1 * num2


def calculate_divide(num1, num2):
    return num1 / num2


def calculate_plus(num1, num2):
    return num1 + num2


def calculate_minus(num1, num2):
    return num1 - num2


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == "+":
            (token, index) = read_plus(line, index)
        elif line[index] == "-":
            (token, index) = read_minus(line, index)
        elif line[index] == "*":
            (token, index) = read_mul(line, index)
        elif line[index] == "/":
            (token, index) = read_divide(line, index)
        # 括弧を読む
        elif line[index] == "(" or line[index] == ")":
            (token, index) = read_parentheses(line, index)
        else:
            print("Invalid character found: " + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# /と*の演算子が来た時の処理
def calculate_mul_divide(tokens, index):
    while index < len(tokens):
        if tokens[index]["type"] == "MUL":
            num1 = tokens[index - 1]["number"]
            num2 = tokens[index + 1]["number"]
            result = calculate_mul(num1, num2)
            tokens[index - 1 : index + 2] = [{"type": "NUMBER", "number": result}]
        elif tokens[index]["type"] == "DIVIDE":
            num1 = tokens[index - 1]["number"]
            num2 = tokens[index + 1]["number"]
            result = calculate_divide(num1, num2)
            tokens[index - 1 : index + 2] = [{"type": "NUMBER", "number": result}]
        else:
            index += 1
    return tokens


# *と/だけを計算して、+と-だけが残った新しいtokenを作る
def evaluate_mul_divide(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "MUL" or tokens[index]["type"] == "DIVIDE":
            tokens = calculate_mul_divide(tokens, index)
        index += 1
    return tokens


def evaluate(tokens):
    answer = 0
    index = 0
    tokens.insert(0, {"type": "PLUS"})
    tokens = evaluate_mul_divide(tokens)
    print(tokens)
    while index < len(tokens):
        if tokens[index]["type"] == "NUMBER":
            if tokens[index - 1]["type"] == "PLUS":
                answer += tokens[index]["number"]
            elif tokens[index - 1]["type"] == "MINUS":
                answer -= tokens[index]["number"]
            else:
                print("Invalid syntax")
                exit(1)
        index += 1
    return answer


def evaluate_parentheses(tokens):
    parentheses_flag = 0
    temp_list = []
    new_list = []
    right_parentheses = 0
    left_parentheses = 0
    index = 0

    while index < len(tokens):
        if tokens[index]["type"] == "PARENTHESES":
            if tokens[index]["PAIR"] == "(":
                left_parentheses += 1
                if left_parentheses == 1:
                    parentheses_flag = 1
            elif tokens[index]["PAIR"] == ")":
                right_parentheses += 1
                if left_parentheses == right_parentheses:
                    parentheses_flag = 0
                    temp_list.pop(0)
                    new_list.append(
                        {
                            "type": "NUMBER",
                            "number": evaluate(evaluate_parentheses(temp_list)),
                        }
                    )
                    temp_list = []
                    left_parentheses = 0
                    right_parentheses = 0
                    index += 1
                    continue

        if parentheses_flag:
            if left_parentheses != right_parentheses:
                temp_list.append(tokens[index])
        else:
            new_list.append(tokens[index])

        index += 1
    return new_list


def test(line):
    tokens = tokenize(line)
    print("Tokens:", tokens)
    tokens = evaluate_parentheses(tokens)
    print("Tokens after parentheses evaluation:", tokens)
    actual_answer = evaluate(tokens)
    print("Actual answer:", actual_answer)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print(
            "FAIL! (%s should be %f but was %f)"
            % (line, expected_answer, actual_answer)
        )


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.0+2")
    test("1.0/2.0")
    test("3.0+4*2/5+3")
    test("3.0/4*2/5+3")
    test("(3+4*(2-1))/5")
    print("==== Test finished! ====\n")


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    print(tokens)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
