import heapq

N, M = list(map(int, input().split()))

min_heap = []
for i in range(N):
    for j, value in enumerate(list(map(int, input().split()))):
        heapq.heappush(min_heap, [-1 * value, i, j])

answer = 0
while min_heap:
    ret = 0
    selected_nodes = [heapq.heappop(min_heap)]
    temp_min_heap = min_heap[:]
    while len(selected_nodes) < 4 and temp_min_heap:
        val, x1, y1 = heapq.heappop(temp_min_heap)

        # 기존에 선택된 노드들과 상하좌우로 붙어 있는지 여부 확인
        can = False
        for selected in selected_nodes:
            _, x2, y2 = selected

            if abs(x1 - x2) == 1 and abs(y1 - y2) == 0:
                can = True
                break
            elif abs(x1 - x2) == 0 and abs(y1 - y2) == 1:
                can = True
                break

        if can:
            selected_nodes.append([val, x1, y1])

    if len(selected_nodes) == 4:
        for val, x, y in selected_nodes:
            ret += val
        if answer > ret:
            answer = ret

print(-1 * answer)