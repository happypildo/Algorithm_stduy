# Sorting - 정렬
> 데이터를 특정한 기준에 따라서 순서대로 나열
> 
- 본 강의에서는 카드가 나열되어 있고, 카드를 정렬한다는 예시로 진행됩니다.
- 오름차순만 고려합니다.

![CARDS](https://prod-files-secure.s3.us-west-2.amazonaws.com/faad244b-bc57-4ada-9bfd-e20cd3691143/206ab49f-287f-4ed6-b357-4b22ccc93dc1/Untitled.png)

<br>

## Selection sorting - 선택 정렬

> 카드를 하나씩 보면서, 볼 때마다 그를 제외한 카드 중 가장 작은 카드와 교환한다.
> 

```python
CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]

def selection_sort():
    for i in range(len(CARDS)):
        min_idx = i
        min_value = CARDS[i]
        for j in range(i+1, len(CARDS)):
            if CARDS[j] < min_value:
                min_value = CARDS[j]
                min_idx = j
        
        CARDS[i], CARDS[min_idx] = CARDS[min_idx], CARDS[i]

selection_sort()
print(CARDS)
```

### 선택 정렬의 시간 복잡도

- 연산 횟수: $N+(N-1)+(N-2)+\cdots+2$
- 시간 복잡도: `O(N^2)`

<br>

## Insertion sorting - 삽입 정렬

> 현재 위치 이전 카드들이 정렬되어 있다는 가정 하에, 현재 카드와 다른 카드들의 값을 비교해 가며 삽입할 위치를 결정하는 알고리즘
> 

### 예제

- [7, 5, 9, 0] 이라는 데이터가 있을 때, <span style="color:orange">카드 5부터 시작하게 됨
    - **앞에는 정렬되어 있다는 가정**</span>
- 5를 보았을 때, 7보다 작기에 <span style="color:orange">**7 앞에 삽입한다**</span>.
    - [5, 7, 9, 0]
- 9를 보았을 때, 5와 7보다 크기 때문에 <span style="color:orange">**가만히 냅둔다**</span>.
- 0을 보았을 때, 5, 7, 9보다 다 작으니 <span style="color:orange">**5 앞에 삽입한다**</span>.
    - [0, 5, 7, 9]

### 코드

```python
def insertion_sort():
    for i in range(1, len(CARDS)):
        for j in range(i, 0, -1):
            if CARDS[j] < CARDS[j - 1]:
                CARDS[j], CARDS[j - 1] = CARDS[j - 1], CARDS[j]
            else:
                break

insertion_sort()
print(CARDS)
CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]
```

### 삽입 정렬의 시간 복잡도

- 앞서 보았던 선택 정렬과 같이 `O(N^2)`의 시간 복잡도를 갖는다.
- 그러나, 현재 카드들이 <span style="color:orange">***거의 정렬되어 있다면***</span> 최선의 경우 `O(N)`을 갖는다.
    - 뒤로 가면서 바꾸는 과정을 거의 안 하기 때문.

<br>

## Quick sorting - 퀵 정렬

> 기준 데이터를 설정하고, 그 기준보다 큰 데이터와 작은 데이터의 위치를 바꿔가며 정렬하는 방식

<br>

### 구체적인 동작 방식
<br>

- 구체적으로는 <span style="color:orange">**Pivot**</span>을 사용한다. (책에서는 호어 분할(Hoare Partition) 방식을 활용하여 첫번째 데이터를 피벗으로 한다.)
- Pivot 이 설정되면,
    - (Pivot 제외) <span style="color:orange">왼쪽부터 Pivot보다 큰 값</span>을 찾고
    - <span style="color:orange">오른쪽부터 Pivot보다 작은 값</span>을 찾는다.
    - 그리고 그 것들을 <span style="color:orange">교환</span>한다.
    
    > 예시)
    > [5 7 9 0 3 1 6] 일 때, Pivot은 5이다.
    > 1. 왼쪽부터 큰 값은 ‘7’, 작은 값은 ‘1’이다.
    > 2. 이 둘을 교환한 결과는 [5 1 9 0 3 7 6]
    > 

### 그렇다면, pivot은 언제 옮기나요?

- <span style="color:orange">‘왼쪽’과 ‘오른쪽’ 값이 교차</span>될 경우가 있다.
    - 앞선 방식을 제대로 수행했다면, <span style="color:orange">**교차 시에는 교차된 값을 기준**</span>으로 <span style="color:orange">***왼쪽은 작은 값들 오른쪽은 큰 값들***</span>이 되게 된다.
    - 이 때, <span style="color:orange">작은 값과 Pivot값을 바꿔주고, 바뀐 Pivot 값 위치를 기준으로 양쪽을 나눠 다시 진행한다</span>.
    
    > 예시)
    > 위 방식에서 쭉 간다면, [5 1 3 0 9 7 6]이 된다.
    > 1. 왼쪽에서 간 값은 ‘9’ 이고 오른쪽에서 간 값은 ‘0’이다. 즉, **교차된다**.
    > 2. 이 때, Pivot 값과 작은 값 ‘0’을 교환한다. [0 1 3 5 9 7 6].
    > 3. Pivot을 기준으로 배열을 나누고, [0, 1, 3], [9, 7, 6]에 대해 똑같이 진행한다.
    > 

![책에 나온 예시.](https://prod-files-secure.s3.us-west-2.amazonaws.com/faad244b-bc57-4ada-9bfd-e20cd3691143/e7e6b655-87d1-4ead-99cb-d66f8324be18/Untitled.png)

책에 나온 예시.

### 구현

```python
CARDS = [7, 5, 9, 0, 3, 1, 6, 2, 4, 8]

def quick_sort(arr):
    if len(arr) == 0 or len(arr) == 1:
        return arr
        
    pivot = 0

    left = 1
    right = len(arr) - 1
    while left < right:
        while left < len(arr) and arr[left] < arr[pivot]:
            left = left + 1
        while right > 0 and arr[right] > arr[pivot]:
            right = right - 1
        
        if left > right:
            arr[pivot], arr[right] = arr[right], arr[pivot]
        else:
            arr[left], arr[right] = arr[right], arr[left]
    
    sorted_arr = quick_sort(arr[:right]) + [arr[right]] + quick_sort(arr[right+1:])

    return sorted_arr

print(quick_sort(CARDS))
```