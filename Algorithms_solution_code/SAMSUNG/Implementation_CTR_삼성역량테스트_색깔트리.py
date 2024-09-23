from collections import deque

# 전체 트리들의 가치를 저장하는 변수 (global 변수로 설정해 사용)
value = 0

class Node:
    def __init__(self, m_id, p_id, color, max_depth):
        """_summary_

        Args: (기본 제공 파라미터)
            m_id (_type_): 노드의 아이디
            p_id (_type_): 부모의 아이디
            color (_type_): 갖고 있는 색
            max_depth (_type_): 최대 깊이
        """
        self.own_id = m_id
        self.parent_id = p_id
        self.color = color
        self.max_depth = max_depth
        
        """_summary_
            child_list: 자식들의 리스트
            color_set: 하위 트리의 색깔 집합 
        """
        self.child_list = []
        self.color_set = {color}


def can_be_merged(node_list, node, depth):
    """_summary_

    Args:
        node_list (_type_): 노드 리스트
        node (_type_): 현재 관심있는 노드
        depth (_type_): max depth와 비교할 현재 depth

    Returns:
        _type_: 재귀함수 형태로 루트까지 올라가면서 depth 제약에 걸리지 않는지 확인
    """
    if node is None:
        return True

    if node.max_depth > depth:
        next_node = node_list[node.parent_id]
        return can_be_merged(node_list, next_node, depth + 1)
    else:
        return False


def add_node(node_list, m_id, p_id, color, max_depth):
    """_summary_

    Args:
        node_list (_type_): 노드 리스트
        m_id (_type_): 넣으려는 노드의 아이디
        p_id (_type_): 붙이려는 노드의 아이디 (부모)
        color (_type_): 색깔
        max_depth (_type_): 최대 깊이
    """
    # 부모 노드와 연결이 된다면, 부모의 constraint에 위반하지 않는지 확인
    # 부모 노드와 연결이 된다면, 부모의 child 정보에 추가
    global value

    if p_id == -1:
        # 부모 아이디가 -1이라면, 스스로 루트가 된다.
        node_list[m_id] = Node(m_id, p_id, color, max_depth)
        value += 1
    else:
        # 부모 아이디가 -1이 아니라면, depth 제약 조건에 걸리지 않는지 확인해야 한다.
        validity = can_be_merged(node_list, node_list[p_id], 1)
        if validity:
            # parent에 연결되어도 된다.
            node_list[m_id] = Node(m_id, p_id, color, max_depth)
            
            # 부모의 child_list에 값을 삽입한다.
            node_list[p_id].child_list.append(m_id)
            
            # 새로 추가되었으니, 이의 가치를 추가해 준다.
            value += 1

            # 새로 추가되었으니, 부모를 타고 올라가면서 색과 global 가치를 업데이트 해야 한다.
            change_color(node_list, m_id, color)


def change_color(node_list, m_id, new_color):
    # 색을 변화시키는 것과, 새로운 노드를 넣었을 때는 동일한 동작을 한다.
    # 색을 변화시키는 것: 서브 트리까지 확인한다.
    # 새로운 노드를 넣는 것: 서브 트리가 형성되어 있지 않기 때문에, 위로만 올라간다.
    global value

    # 먼저, 아래로 내려가면서 색과 가치를 업데이트 한다.
    new_set = {new_color}
    queue = deque([m_id])

    while queue:
        idx = queue.popleft()

        # 가치 업데이트
        if len(node_list[idx].color_set) != 1:
            # 현재 노드의 color set 길이가 1이 아니라는 것은, 하위 트리에 겹치지 않는 색이 있다는 것
            # 그러나 색이 하나로 통일되기 때문에, 이전 가치를 빼고 새로운 가치(1)를 더해준다.
            value -= len(node_list[idx].color_set) ** 2
            value += 1

        node_list[idx].color_set = new_set
        node_list[idx].color = new_color

        for child in node_list[idx].child_list:
            # 색이 이미 변화시킬 색과 동일하다면 굳이 바꾸지 않아도 된다.
            if node_list[child].color_set == new_set:
                continue
            queue.append(child)

    # 다음으로, 부모로 올라가면서 그들의 색과 가치를 업데이트 한다.
    parent = node_list[m_id].parent_id
    parent = node_list[parent]

    while parent is not None:
        # 자식들의 색깔을 수집해서 color set을 업데이트한다.
        merged_color_set = {parent.color}
        for child in parent.child_list:
            merged_color_set = merged_color_set.union(node_list[child].color_set)

        # 근데 만약 이전 color set과 바뀌게 될 color set이 같다면, 그 위부터는 볼 필요 없다.
        if parent.color_set == merged_color_set:
            break

        # 가치 갱신 (이전 가치를 빼고 새로운 가치를 더한다.)
        value -= len(parent.color_set) ** 2
        value += len(merged_color_set) ** 2
        
        # color set 갱신
        parent.color_set = merged_color_set

        parent = node_list[parent.parent_id]


# 마지막 하나는 루트 상징 (-1 인덱스)
nodes = [None for _ in range(100002)]

Q = int(input())

for _ in range(Q):
    orders = list(map(int, input().split()))

    if orders[0] == 400:
        print(value)
    elif orders[0] == 100:
        # 삽입 연산
        add_node(nodes, orders[1], orders[2], orders[3], orders[4])
    elif orders[0] == 200:
        # 색깔 변경
        change_color(nodes, orders[1], orders[2])
        pass
    elif orders[0] == 300:
        # 색깔 조회
        print(nodes[orders[1]].color)