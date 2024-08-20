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


                