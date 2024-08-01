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