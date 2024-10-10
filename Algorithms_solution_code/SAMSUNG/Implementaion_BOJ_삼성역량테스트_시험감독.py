import math

N = int(input())
num_of_tester = list(map(int, input().split()))
B, C = list(map(int, input().split()))

num_of_observers = 0
for num in num_of_tester:
    num -= B

    num_of_observers += 1
    if num > 0:
        num_of_observers += math.ceil(num / C)

print(num_of_observers)
