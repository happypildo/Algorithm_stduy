# Implementation - 구현

> 머리 속에 있는 알고리즘을 코드로 구현하는 과정
> 
- 상당히 간단한 정의인데, 예시를 보면 감이 잡힌다.
    - 알고리즘은 간단한데 예외처리가 많은 문제
    - 특정 소수점 자리까지 출력하는 문제
    - 문자열 파싱 문제
- 이들은 크게 완전 탐색과 시뮬레이션으로 나뉠 수 있다. (다 그렇지는 않다.)

| 완전 탐색 | 시뮬레이션 |
| --- | --- |
| 모든 경우의 수를 다 계산 | 문제에서 제시한 알고리즘을 한 단계씩 직접 수행 |

## 구현에서 고려해야할 사항

1. <span style="color:red">메모리 제약 사항</span>
- 파이썬은 직접 자료형을 지정할 필요가 없기에 **매우 큰 수의 연산을 기본적으로 지원**한다.
- 따라서, 자료형 별 값의 범위, 크기를 `java` 기준으로 작성해 보겠다.

| 자료형 종류 | 자료형의 크기 | 자료형의 범위 |
| --- | --- | --- |
| byte | 1 B | -2^7 ~ 2^7 - 1 |
| short | 2 B | -2 ^ 15 ~ 2^15 - 1 |
| int | 4B | -2 ^ 31 ^ 2^31 - 1 |
| long | 8 B | -2^63 ~ 2^63 - 1 |
| float | 4 B (부동소수점) | -3.4e+38 ~ 3.4e+38 |
| double | 8 B (부동소수점) | -1.79e308 ~ 1.79e308 |
- <span style="color:red">참고로, java에는 unsigned 형이 없다.</span>

1. 실행 속도 (계산 복잡도)
- 코딩 테스트 환경에서는 파이썬이 <span style="color:red">**1초에 2000만번 연산을 수행**</span>한다고 가정하면 큰 무리가 없다.
    - 즉, 1초라는 시간 제약이 있는 문제에서, 계산 복잡도가 `O(Nlog(N))` 이라 할 때, 최대 연산 횟수가 100만이라면 문제가 없다.
    → `O(Nlog(N))` 에서 `N=1,000,000` 일 때, `20,000,000` 임


## 예제 1. 상하좌우

> (0, 0)에서 여행을 시작하여 주어진 방향(상, 하, 좌, 우)으로 이동을 진행한다.
여기서, 지도의 크기 N $\times$ N 을 넘을 수 없기에 이를 넘는 방향은 무시한다.
주어진 모든 방향을 이동했을 때, 최종 위치를 반환하시오
> 

```python
DIRECTION = {
    'U': [-1, 0],
    'D': [1, 0],
    'L': [0, -1],
    'R': [0, 1]
}

N = int(input())
moving_directions = input().split()
current_location = [0, 0]

for direction in moving_directions:
    dx, dy = DIRECTION[direction]

    temp_x = current_location[0] + dx
    temp_y = current_location[1] + dy

    if temp_x < 0 or temp_x > N - 1:
        continue
    elif temp_y < 0 or temp_y > N - 1:
        continue
    else:
        current_location[0] = temp_x
        current_location[1] = temp_y

print(current_location[0] + 1, current_location[1] + 1)
```

- 시간 복잡도는 단순히 `O(N)`이다.

## 예제 2. 미생물 군집 이동

> 문제 설명이 길다. 다음 링크를 참고하자. <br>
> https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AV597vbqAH0DFAVl

```python
DIRECTION = {
    1: [-1, 0],
    2: [1, 0],
    3: [0, -1],
    4: [0, 1]
}
 
 
def change_direction(in_direction):
    if in_direction == 1:
        return 2
    elif in_direction == 2:
        return 1
    elif in_direction == 3:
        return 4
    else:
        return 3
 
 
class Cluster:
    def __init__(self, N, x, y, num_of_microbe, direction):
        self.map_size = N
        self.location_x = x
        self.location_y = y
        self.num_of_microbe = num_of_microbe
        self.direction = direction
        self.is_alive = True
 
    def move_cluster(self):
        dx, dy = DIRECTION[self.direction]
 
        self.location_x = self.location_x + dx
        self.location_y = self.location_y + dy
 
        if self.location_x < 1 or self.location_x > self.map_size - 2:
            self.num_of_microbe = int(self.num_of_microbe / 2)
            self.direction = change_direction(self.direction)
        elif self.location_y < 1 or self.location_y > self.map_size - 2:
            self.num_of_microbe = int(self.num_of_microbe / 2)
            self.direction = change_direction(self.direction)
 
        if self.num_of_microbe == 0:
            self.is_alive = False
 
 
def merge_cluster(clusters):
    new_cluster = Cluster(
        N=clusters[0].map_size,
        x=clusters[0].location_x,
        y=clusters[0].location_y,
        num_of_microbe=clusters[0].num_of_microbe,
        direction=0
    )
 
    num_of_microbe_for_each_cluster = [c.num_of_microbe for c in clusters]
 
    max_idx = num_of_microbe_for_each_cluster.index(max(num_of_microbe_for_each_cluster))
 
    new_cluster.num_of_microbe = sum(num_of_microbe_for_each_cluster)
    new_cluster.direction = clusters[max_idx].direction
 
    return new_cluster
 
 
# main
T = int(input())
 
for t_iter in range(1, T+1):
    N, M, K = list(map(int, input().split()))
 
    cluster_lists = []
    for k_iter in range(K):
        x, y, num_of_microbe, direction = list(map(int, input().split()))
        cluster_lists.append(Cluster(N=N, x=x, y=y, num_of_microbe=num_of_microbe, direction=direction))
 
    for m_iter in range(M):
        loc_of_clusters = []
 
        # 군집 이동 후 위치 저장
        for idx, cluster in enumerate(cluster_lists):
            cluster.move_cluster()
            loc_of_clusters.append("000"+str(cluster.location_x)+"_"+str(cluster.location_y)+"000")
 
            # if not cluster.is_alive:
            #     del cluster_lists[idx]
            #     del loc_of_clusters[idx]
 
        # 저장된 위치 기반 동일한 위치 추출
        loc_dict = {loc: [] for loc in loc_of_clusters}
        for idx, loc in enumerate(loc_of_clusters):
            loc_dict[loc].append(idx)
 
        # 동일한 위치에 있는 군집 합치기
        temp_cluster_lists = []
        for dict_idx, loc_dict_key in enumerate(loc_dict.keys()):
            if len(loc_dict[loc_dict_key]) > 1:
                clusters_to_merge = []
                for idx in loc_dict[loc_dict_key]:
                    clusters_to_merge.append(cluster_lists[idx])
 
                temp_cluster_lists.append(merge_cluster(clusters_to_merge))
            else:
                for idx in loc_dict[loc_dict_key]:
                    temp_cluster_lists.append(cluster_lists[idx])
 
        cluster_lists = temp_cluster_lists
 
    sum_of_microbe = 0
    for cluster in cluster_lists:
        sum_of_microbe = sum_of_microbe + cluster.num_of_microbe
 
    print(f"#{t_iter} {sum_of_microbe}")
```

## 예제 3. 하노이 탑

> 익히 잘 알려져 있는 예제이다. 이를 재귀로 풀고자 했다.
> 

```python
def hanoi(N, start_poll, end_poll, middle_poll):
    result = ""

    if N == 1:
        return f"{start_poll} {end_poll}\n"

    result = result + hanoi(N-1, start_poll=start_poll, end_poll=middle_poll, middle_poll=end_poll)
    result = result + f"{start_poll} {end_poll}\n"
    result = result + hanoi(N-1, start_poll=middle_poll, end_poll=end_poll, middle_poll=start_poll)

    return result

N = int(input())

if N > 20:
    print(2 ** N - 1)
else:
    print(2 ** N - 1)
    print(hanoi(N=N, start_poll=1, end_poll=3, middle_poll=2))

```

<br>

## 재귀로 풀 수 있는 간단한 예시들

### 순열 - Permutation

> 숫자를 나열한 것 ( A = (1, 2, 3) ≠ (1, 3, 2) )
> 
- 수학적 표현: $nPr = n \times (n - 1) \times \dots \times (n - r + 1)$


```python
# 단순 반복문
for i in range(1, 4):
	for j in range(1, 4):
		if j != i:
			for k in range(1, 4):
				if k != i and k != j:
					print(i, j, k)
					
# 재귀
# selected: 선택된 값의 목록
# remain: 남은 것들
def perm(selected, remain):
	if not remain:
		print(selected)
	else:
		for i in range(len(remain)):
			select_i = remain[i]
			remain_list = remain[:i] + remain[i+1:]
			perm(selected + [select_i], remain_list)
```

<br>

### 조합

> 순서 없이 숫자를 나열한 것 ( A = (1, 2, 3) == (2, 3, 1) )
> 
- 수학적 표현: $nCr = \frac{n!}{(n-r)!r!}$
- 재귀적 표현: $nCr = (n-1)C(r-1) + (n-1)C(r)$

```python
# 단순 for문
for i in range(1, 5):
	for j in range(i, 5):
		for k in range(j, 5):
			print(i, j, k)
			
# 재귀
def comb(arr, n):
	result = []
	if n == 1:
		return [[i] for i in arr]
	
	for i in range(len(arr)):
		elem = arr[i]
		for rest in comb(arr[i+1:], n-1):
			result.append([elem] + rest)
	
	return result
```

- 재귀 형태에서 중요한 아이디어는 다음과 같다.
    - {3, 4}에서 1개를 고를 때 → [3], [4]
    - {2, 3, 4}에서 2개를 고를 때 → **[2, 3]**, **[2, 4]**, **[3, 4]**
    - {1, 2, 3, 4}에서 3개를 고를 때 → [1, **2, 3**], [1, **2, 4**], [1, **3, 4**], …
    - **나만 선택되면 하위 문제랑 동일해 지는 것이다.**

<br>

### 부분 집합

> 집합에 포함된 원소들을 선택 ( A = {(1, 2, 3), (2, 3)} )
> 
- 각 원소에 대해, **부분 집합에 포함할 것이냐 아니냐**, 2개의 경우의 수가 있음 (멱집합)

```python
selected = [0] * 3

for i in range(2):
	selected[0] = i
	for j in range(2):
		selected[1] = i
		for m in range(2):
			selected[2] = m
			subset = []
			for n in range(3):
				if selected[n] == 1:
					subset.append(n+1)
			print(subset)
```

- 앞서 언급된 포함되느냐/안 되느냐를 중첩 for문으로 구현
- 원소의 개수가 바뀔 때, **for문의 중첩 개수가 늘어나**야 함

- 재귀 구현

```python
subsets = []

def generate_subset(depth, included):
	global subsets
	
	if depth == len(input_list):
		cnt_subset = [input_list[i] for i in range(len(input_list)) if included[i]]
		subsets.append(cnt_subset)
		
		return
		
	included[depth] = False
	generate_subset(depth + 1, included)
	
	included[depth] = True
	generate_subset(depth + 1, included)
```
