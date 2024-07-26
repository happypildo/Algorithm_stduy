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

def DFS(node):
    global graph
    global stack

    print(node)
    
    is_there_to_go = False
    for to_go_idx in graph[node]:
        if to_go_idx not in is_visited:
            stack.push(to_go_idx)
            is_visited.add(to_go_idx)
            DFS(to_go_idx)
            is_there_to_go = True

    if not is_there_to_go:
        stack.pop()
      
start_node_idx = 0
is_visited.add(start_node_idx)
DFS(start_node_idx)

print("END")