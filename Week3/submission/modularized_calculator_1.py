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
        token = {"type": "OPEN_PARENTHESES"}
    else:
        token = {"type": "END_PARENTHESES"}
    return token, index + 1


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


# *と/だけを計算して、+と-だけが残った新しいtokenを作る
def evaluate_mul_divide(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]["type"] == "MUL" or tokens[index]["type"] == "DIVIDE":
            while index < len(tokens):
                if tokens[index]["type"] == "MUL":
                    num1 = tokens[index - 1]["number"]
                    num2 = tokens[index + 1]["number"]
                    result = num1 * num2
                    tokens[index - 1 : index + 2] = [
                        {"type": "NUMBER", "number": result}
                    ]
                elif tokens[index]["type"] == "DIVIDE":
                    num1 = tokens[index - 1]["number"]
                    num2 = tokens[index + 1]["number"]
                    result = num1 / num2
                    tokens[index - 1 : index + 2] = [
                        {"type": "NUMBER", "number": result}
                    ]
                else:
                    index += 1
        index += 1
    return tokens


def evaluate_plus_minus(tokens):
    answer = 0
    index = 0
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


def evaluate(tokens):
    tokens.insert(0, {"type": "PLUS"})
    tokens = evaluate_parentheses(tokens)
    tokens = evaluate_mul_divide(tokens)
    answer = evaluate_plus_minus(tokens)
    return answer


# 他の解き方　再帰じゃなくする括弧の位置のインデックスを保存していく　コピーをするとコストがかかる
def evaluate_parentheses(tokens):
    temp_list = []
    new_list = []
    parentheses_level = 0
    index = 0
    while index < len(tokens):
        if tokens[index]["type"] == "OPEN_PARENTHESES":
            parentheses_level += 1
        elif tokens[index]["type"] == "END_PARENTHESES":
            parentheses_level -= 1
            if parentheses_level == 0:
                temp_list.pop(0)
                new_list.append(
                    {
                        "type": "NUMBER",
                        "number": evaluate(temp_list),
                    }
                )
                temp_list = []
                index += 1
                continue
        if parentheses_level != 0:
            temp_list.append(tokens[index])
        else:
            new_list.append(tokens[index])
        index += 1
    return new_list


def test(line):
    tokens = tokenize(line)
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
    test("1")
    test("1+2")
    test("1.0+2.0")
    test("1.0+2")
    test("1.0+2.1-3")
    test("1.0/2.0")
    test("2.2*3.4")
    test(
        "3.0+4*2/5+3"
    )  # 足し算の間に掛け算だけががある場合や、3つ目のブロックも足し算掛け算があるといい
    test("(3+4*(2-1))/5")  # 1重括弧のテスト、3重括弧のテスト
    print("==== Test finished! ====\n")
    # 0と1と2以上の3パターンは考えたい


run_test()

while True:
    print("> ", end="")
    line = input()
    tokens = tokenize(line)
    print(tokens)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)

# 本質としては、関数の始まりから終わりをevaluateで計算して一つの数字に置き換える
# 括弧の役割を共通化するとシンプルになる
# 処理もコードベースで考えるんじゃなくて、具体的に何をしてるのかをを追ってみる
