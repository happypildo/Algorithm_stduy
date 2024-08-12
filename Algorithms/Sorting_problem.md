# Sorting - 문제 풀이

- 앞선 포스트에서 여러 정렬 알고리즘을 배웠다.
- 하지만 Python은 **딸깍**의 신이다.

<br>

# 파이썬 정렬 라이브러리 - `sorted()`

> 최악의 경우에도 `O(NlogN)`을 보장하는 형태이다. (병합 정렬 기반)
> 

```python
array = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]

result = sorted(array)
# array(sort) -> 이 방식은 array 자체에 정렬을 가하는 방식이다.
# 파이썬의 정렬은 기본적으로 오름차순이다.
```

## `Key`

> `sorted`, `sort`의 매개 변수로서, **정렬의 기준**이 된다.
> 

```python
array = [('banana', 2), ('apple', 5), ('carrot', 3)]

def setting(data):
	return data[1]
	
result = sorted(array, key=setting)
# ('banana', 2), ('carrot', 3), ('apple', 5)
```

### 활용 예시 - 정렬된 배열의 이전 인덱스 가져오기

> 가끔 문제풀 때 필요한 개념이다. `numpy`에는 딸깍이 존재했는데 내장 라이브러리로는 `key`를 사용하면 된다.
> 

```python
array = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]

result = sorted([i for i in range(len(array))], key=lambda k: array[k])
```

# 정렬 문제의 유형

1. 정렬 라이브러리로 풀 수 있는 문제
2. 정렬 알고리즘의 원리에 대해서 물어보는 문제
3. 더 빠른 정렬이 필요한 문제

## 유형 1. - 라이브러리 활용

```python
"""
이름과 점수가 있을 때, 점수 순으로 이름을 출력
"""

names = ['A', 'B', 'C']
scores = [10, 30, 20]

name_score = []
for n, s in zip(names, scores):
    name_score.append([n, s])

sorted_names_to_scores = sorted(name_score, key=lambda k: k[1])
print(sorted_names_to_scores)
```

```python
"""
A와 B 배열의 요소를 K 번 바꿔치기 해가며, A 원소의 총 합을 최대로 만들고 싶다.
이 때, A 원소 총 합의 최댓값을 구하시오.
"""

A = [1, 2, 5, 4, 3]
B = [5, 5, 6, 6, 5]

A = sorted(A)
B = sorted(B, reverse=True)

k_cnt = 0
K = 3
answer = 0
for a, b in zip(A, B):
    if k_cnt < K:
        answer = answer + b
    else:
        answer = answer + a
    k_cnt += 1

print(answer)
```