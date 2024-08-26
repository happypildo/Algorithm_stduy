"""
# 문제 설명:
- 여러 길이의 가래떡 N개가 있다.
- 이를 일자로 나열하여 한 번 자르고 나머지 길이를 최소 M이상으로 하고 싶다.
    - 이 때, M에 최대한 가깝게 즉, 잘려진 길이와 M의 차이가 최소로 하는 자름 길이를 구하시오.

# 접근 방법:
- 이분 탐색으로 진행한다.
    - 입력이 매우 크다고 해보자. 즉, 떡의 길이가 최대 10억, 떡의 개수가 1,000,000이다.
    - 굉장히 커 보이지만 이분 탐색의 경우 `log(N)`이기 때문에, 대략 31회 정도 걸린다.
    - 그러면 대략 3천만번 계산을 하게 되고, 2초가량 연산을 진행할 수 있다.
"""
N, M = list(map(int, input().split()))

array = list(map(int, input().split()))

start = 0
end = max(array)

rsult = 0
while start <= end:
    total = 0
    mid = (start + end) // 2
    for x in array:
        if x > mid:
            total += x - mid
        
        if total < m:
            end = mid - 1
        else:
            result = mid
            start = mid + 1

print(result)