## 순차 탐색 - Sequential Search

> 앞에서부터 데이터를 하나 씩 찾아보자.
> 
- 이 방법은 단순하고 복잡도도 `O(N)` 이다.
    - 특히, 해당 방법은 python 내부 함수인 `.count()`에서 사용된다.

```python
def sequential_sort(arr, target):
    ret = []
    for idx, elem in enumerate(arr):
        if elem == target:
            ret.append(idx)
    return ret

data = ["Hi", "My", "Name", "Is", "Pildo"]
print(sequential_sort(data, "My"))
```

## 이진 탐색 - Binary Search

> 반씩 쪼개면서 찾아보자.
> 
- 이 알고리즘은 정렬된 형태의 데이터에서, 쉽게 데이터를 찾을 수 있는 방법이다.

### 간단한 예시

- 다음과 같은 데이터가 있다고 해보자
    
    ```python
    data = [1, 2, 3, 4, 5, 6]
    ```
    
- [순차 탐색]에서는 이중 `5`라는 값을 찾기 위해서 앞에서 부터 찾아 나갈 것이다.
    - 만약 데이터가 크고, 값이 뒤에 있다면 `O(N)`도 꽤나 큰 복잡도로 다가올 것이다.
- 데이터가 정렬되어 있으니, ‘절반’을 먼저 보자.
    
    ```python
    half1 = [1, 2, 3]
    half2 = [4, 5, 6]
    ```
    
- 이 중 `5`는 half2에 있다. 그러면, half2도 절반으로 나눠보자.
    
    ```python
    half1 = [4, 5]
    half2 = [6]
    ```
    
- 이 중 `5` 는 half1에 있다. 또 반으로 나누자.
    
    ```python
    half1 = [4]
    half2 = [5]
    ```
    
- 답이 나왔다!

### 재귀로 구현해보자!

- 위와 같이, 개념자체는 복잡하지 않다. 하지만 늘 그렇듯 코드로 구현하기는 다르다.

```python
def binary_search(arr, target):
    if len(arr) == 0:
        return 0
    
    middle_idx = len(arr) // 2

    if arr[middle_idx] == target:
        return middle_idx
    elif arr[middle_idx] > target:
        # 데이터는 왼쪽 반에 위치한다.
        return binary_search(arr[:middle_idx], target)
    elif arr[middle_idx] < target:
        # 데이터는 오른쪽 반에 위치한다.
        return middle_idx + 1 + binary_search(arr[middle_idx+1:], target)

data = [1, 2, 3, 4, 5, 6]
print(binary_search(data, 4))
```

### 이진 탐색 트리

> 트리 개념은 여기를 참고하자 [이진 트리 구현](https://www.notion.so/4ae27fc7d7c343e3a69e4d5a551934ef?pvs=21)
> 

```python
class Node:
    def __init__(self, value, left_child=None, right_child=None):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

class BinaryTree:
    def __init__(self):
        self.Head = None

    def is_empty(self):
        return self.Head is None
    
    def insert(self, node):
        if self.is_empty():
            self.Head = node
        else:
            # 적절한 위치를 찾아주자
            curr_node = self.Head
            while True:
                if curr_node.value < node.value:
                    if curr_node.right_child is None:
                        curr_node.right_child = node
                        break
                    else:
                        curr_node = curr_node.right_child
                else:
                    if curr_node.left_child is None:
                        curr_node.left_child = node
                        break
                    else:
                        curr_node = curr_node.left_child

    

    def traversal(self, node):
        # preorder, V, L, R
        if self.is_empty() or node is None:
            return False
        else:
            print(node.value)
            self.traversal(node.left_child)
            self.traversal(node.right_child)

    def find_value(self,value):
        if self.is_empty():
            return None
        else:
            curr_node = self.Head
            while curr_node is not None:
                if curr_node.value == value:
                    return curr_node
                elif curr_node.value < value:
                    curr_node = curr_node.right_child
                else:
                    curr_node = curr_node.left_child

## Generate Tree
Nodes = [
    Node(30), Node(17), Node(48), Node(5), Node(23), Node(37), Node(50)
]

Tree = BinaryTree()
for node in Nodes:
    Tree.insert(node)

print("Preorder Traversal >> ")
Tree.traversal(Tree.Head)
print("-" * 10)

print()
print("Find a value")
print("\t Find [5] > ", Tree.find_value(5))
print("\t Find [15] > ", Tree.find_value(15))
```

## Python Input 꿀팁

> 데이터의 개수가 매우 많다면, 이 데이터를 받는데에만 꽤나 많은 시간을 사용하게 된다.
> 

```python
import sys

# rstript()은 개행문자를 무시하기 위함이다.
input_data = sys.stdin.readline().rstrip()

print(input_data)
```

- 위 방법은 전체 입력을 한 번에 받는 방식이다. 따라서, 이후 전처리가 필요하긴 하다.