# DFS and BFS

> 탐색이란 자료 구조에 저장된 많은 양의 데이터 중 원하는 데이터를 찾아가는 과정
> 
- 자료 구조: 데이터를 표현하고 관리하고, 처리하기 위한 구조
    - 대표적으론 스택과 큐가 있다.
        - 스택과 큐는 여기 페이지에 정리가 되어 있다: [SW 문제해결](https://www.notion.so/SW-73fe074e068a4198a3b7d17952910202?pvs=21)
    - 이들을 사용할 때는 **오버플로**와 **언더플로**를 고려해야 한다.
        - Overflow: 자료구조가 가득 차 있어, 수용할 수 없는 양의 데이터가 들어올 경우
        - Underflow: 자료구조가 비어 있는데, 삭제 연산을 진행할 경우

        
## Depth-First Search

> 그래프에서 깊은 부분을 우선적으로 탐색하는 알고리즘
> 

### **동작 과정**

1. 탐색 시작 노드를 스택에 삽입하고 방문 처리를 한다.
2. 스택의 최상단 노드에 방문하지 않은 인접 노드가 있으면, 그 인접 노드를 스택에 넣고 방문 처리를 한다.
    1. 방문하지 않은 인접 노드가 없으면, 스택에서 최상단 노드를 꺼낸다.
3. 이를 반복하여, 더 이상 수행할 수 없을 때 종료한다.

### 왜?

- 왜 스택을 사용할까?
    - 스택은 LIFO 형태이기 때문에, 깊은 부분(스택에 마지막에 들어가는)을 먼저 탐색하는 DFS에게 안성맞춤이다.
- 왜 스택에 들어가기 전 방문 처리를 하는 것인가?
    - 스택에 들어간 후 실제 방문 시 방문 처리를 하게 되면, 스택에 중복적으로 노드 정보가 들어갈 수 있다.

### 구현 - 1 - without stack

```python
N = 7

graph = {
    0: [1, 2, 3],
    1: [0, 4],
    2: [0, 5],
    3: [0, 6],
    4: [1],
    5: [2],
    6: [3]
}

is_visited = [0 for _ in range(N)]

def DFS(node):
    global graph
    global is_visited

    print(f"{node} - ", end="")

    for to_go in graph[node]:
        if is_visited[to_go] == 0:
            is_visited[to_go] = 1
            DFS(to_go)

is_visited[0] = 1
DFS(0)
print("END")
```

### 구현 - 2 - with stack

```python
class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0
    
    def pop(self):
        if self.is_empty():
            return False
        else:
            return self.stack.pop()
    
    def push(self, item):
        self.stack.append(item)
    
    def peek(self):
        if self.is_empty():
            return False
        else:
            return self.stack[-1]

N = 7

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1, 5],
    4: [1, 2, 5],
    5: [3, 4, 6],
    6: [5]
}

is_visited = set()
stack = Stack()
stack.push(0)

def DFS(node, stack, is_visited):
    while not stack.is_empty():
        node = stack.peek()
        print(node)

        is_there_to_go = False
        for to_go in graph[node]:
            if to_go not in is_visited:
                is_visited.add(to_go)
                stack.push(to_go)
                is_there_to_go = True
                break

        while not is_there_to_go and not stack.is_empty():
            node = stack.pop()
            for to_go in graph[node]:
                if to_go not in is_visited:
                    is_there_to_go = True
                    stack.push(to_go)
                    break
      
start_node_idx = 0
is_visited.add(start_node_idx)
DFS(start_node_idx, stack, is_visited)

print("END")
```

## BFS - Breadth First Search

> 현재 노드에서 가까운(인접한) 노드부터 우선적으로 탐색하는 알고리즘

<br>


### 동작 과정

1. 탐색 시작 노드를 <span style="color:red">**큐**</span>에 삽입하고 방문 처리를 한다.
2. 큐에서 노드를 꺼내, 해당 노드의 <span style="color:red">인접 노드 중 방문하지 않은 노드</span>를 모두 큐에 삽입한다.
3. 2번 과정을 더 이상 수행할 수 없을 때까지 반복한다.
<br>
<br>
### 왜?

- 방문 처리를 큐에 넣자마자 하는 이유는 이전과 동일하다. 중복된 노드가 들어가지 않기 위함
- 큐에 넣는 이유는, <span style="color:red">**인접한 노드(먼저 큐에 넣은 노드)를 우선적으로 탐색**</span>하기 위함이다.
<br>
<br>
### 참고

- 파이썬에서 `list`를 활용해 `queue`를 만들게 되면, `pop(0)` 함수 사용 시 복잡도는 `O(N)`이다.
    - 맨 앞 원소를 삭제하고, 이어 붙이기 때문.
- 따라서, `from collections import deque`를 사용하자.
    - `linked list`를 활용하기 때문에, 삭제 시에도 복잡도는 `O(1)`이다.
- 코딩 테스트에서는 보통 DFS보다 <span style="color:red">**BFS 구현이 조금 더 빠르게 동작**</span>한다.
    - 재귀 함수 특성으로 인해 프로그램 수행 시간이 다소 느려질 수 있다.

### 구현

```python
from collections import deque

# graph = {
#     0: [1, 2, 3],
#     1: [0, 4],
#     2: [0, 5],
#     3: [0, 6],
#     4: [1],
#     5: [2],
#     6: [3]
# }
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4],
    3: [1, 5],
    4: [1, 2, 5],
    5: [3, 4, 6],
    6: [5]
}

def BFS(graph, start_node):
    result = [start_node]

    is_visited = set()
    is_visited.add(start_node)
    
    queue = deque([start_node])

    while queue:
        current_node = queue.popleft()

        for next_node in graph[current_node]:
            if next_node not in is_visited:
                queue.append(next_node)
                is_visited.add(next_node)
                result.append(next_node)

    return result

print(BFS(graph, 0))
```