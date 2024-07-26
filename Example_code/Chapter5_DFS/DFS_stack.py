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