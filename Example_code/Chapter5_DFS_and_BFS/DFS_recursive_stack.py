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
    0: [1, 2, 3],
    1: [0, 4],
    2: [0, 5],
    3: [0, 6],
    4: [1],
    5: [2],
    6: [3]
}

is_visited = [0 for _ in range(N)]
stack = Stack()
stack.push(0)
is_visited[0] = 1

def DFS(node):
    global graph
    global is_visited
    global stack

    while not stack.is_empty():
        node = stack.peek()
        print(node) 

        is_there_to_go = False
        for to_go in graph[node]:
            if is_visited[to_go] == 0:
                is_visited[to_go] = 1
                stack.push(to_go)
                is_there_to_go = True

        while not is_there_to_go and not stack.is_empty():
            node = stack.pop()
            for to_go in graph[node]:
                if is_visited[to_go] == 0:
                    is_there_to_go = True

    

DFS(0)
print("END")