import functools
import re


def exam1(input_a, input_b):
    idx = 0;
    for x in input_a:
        # Check char idx if match at same idx will return INVALID result
        if x == input_b[idx]:
            return False
    return True


def exam2(number):
    match = list(filter(lambda x: number % x == 0, [x for x in range(1, number)]))
    result = functools.reduce(lambda x, y: x + y, match, 0)
    if result > number:
        return "abundant"
    elif result < number:
        return "deficient"
    return "perfect"


def exam3(text):
    data = ''.join(text.split(" "))
    return bytes.fromhex(data).decode('utf-8')


def exam5(text):
    all_text = text.split('\n')
    acc = 0
    for x in all_text:
        r = re.findall("/\\\\", x)
        acc += len(r)
    return acc


def exam6(number):
    result = [number]
    expect = number

    while expect > 1:
        if expect % 2 == 0:
            expect = expect / 2
        else:
            expect = (expect * 3) + 1
        result.append(int(expect))

    return result
    # not complete


def exam7(depth, msg):
    if depth == 1:
        return msg
    current = msg;
    result = ["" for x in range(depth)]
    while True:
        z = current[:depth]
        current = current[depth:]
        if len(z) < 1:
            break;

        for x in range(depth):
            try:
                result[x] += z[x]
            except Exception as e:
                result[x] += 'x'
    return result


if __name__ == '__main__':
    print("=========Exam 1")
    print(exam1("1234", "4426"))
    print(exam1("1234", "4426"))
    print("==========Exam 2")
    print(exam2(6))
    print(exam2(15))
    print(exam2(18))
    print("==========Exam 3")
    print(exam3("48 65 6C 6C 6F 20 77 6F 72 6C 64 21"))
    print(exam3("43 6F 64 69 6E 47 61 6D 65 20 72 6F 63 6B 27 73"))
    print("==========Exam 5")
    sample = "     /\     \n" \
             "  /\/   \    \n" \
             " /       \    "
    print(exam5(sample))
