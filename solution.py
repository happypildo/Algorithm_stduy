import decimal

def calculate_(A, B):
    # (A + B)! / (A! B!)
    # print(A, B, end = " ")

    if A < B:
        A, B = B, A
    ret = decimal.Decimal('1')
    cnt = 0
    denominator = [i for i in range(1, B+1)]
    for i in range(A + 1, A + B + 1):
        ret *= i
        if cnt < len(denominator):
            ret /= denominator[cnt]
            # ret = round(ret)
            cnt += 1
    # print(ret)

    return ret
N = int(input())
num_of_1 = N
num_of_2 = 0

answer = 0

while True:
    if num_of_1 < 0 or num_of_2 < 0:
        break
    answer += calculate_(num_of_1, num_of_2)%10007
    num_of_1 -= 2
    num_of_2 += 1
print(int(answer % 10007))
# print(answer % 10007)
# if answer != int(answer):
#     print(i)

