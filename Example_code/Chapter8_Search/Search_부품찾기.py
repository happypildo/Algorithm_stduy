# 파이썬 딸깍 버전
input_data = [
    5,
    "8 3 7 9 2",
    3,
    "3 7 2"
]
N = input_data[0]
elements = set(input_data[1].split())
M = input_data[2]
target_elements = input_data[3].split()

flag = True
for elem in target_elements:
    if elem not in elements:
        flag = False
        break

if flag:
    print("Yes")
else:
    print("No")

# 파이썬 노가다 버전
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

    def find_value(self, value):
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

N = input_data[0]
elements = set(input_data[1].split())
M = input_data[2]
target_elements = input_data[3].split()

tree = BinaryTree()
for elem in elements:
    tree.insert(Node(elem))

flag = True
for tar_elem in target_elements:
    if tree.find_value(tar_elem) is None:
        flag = False
        break

if flag:
    print("Yes")
else:
    print("No")

"""
5
8 3 7 9 2
3
5 7 9
"""