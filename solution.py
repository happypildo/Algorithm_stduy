fastest_path = ""
def DFS(source, path_dict, ticket_set, used_ticket, travel):
    global fastest_path
    if path_dict.get(source, None) is None:
        if len(travel) == len(ticket_set) * 3 * 2:
            if fastest_path > travel:
                fastest_path = travel
        return
    if len(travel) == len(ticket_set) * 3 * 2:
        if fastest_path > travel:
            fastest_path = travel
        return
    # if travel > fastest_path:
    #     return
    
    for destination in path_dict[source]:
        if (source, destination) not in used_ticket:
            temp_used_ticket = used_ticket | set([(source, destination)])

            DFS(destination, path_dict, ticket_set, temp_used_ticket, travel + f"{source}{destination}")


def solution(tickets):
    global fastest_path

    path_dict = {}
    ticket_set = set()
    for source, destination in tickets:
        ticket_set.add((source, destination))
        if path_dict.get(source, None) is None:
            path_dict[source] = [destination]
        else:
            path_dict[source].append(destination)

    # for key in path_dict.keys():
    #     path_dict[key] = sorted(path_dict[key])

    fastest_path = "a" * len(ticket_set) * 3 * 2
    DFS(source="ICN", path_dict=path_dict, ticket_set=ticket_set, used_ticket=set(), travel="")
    
    # PROCESSING
    answer = []
    for offset in range(0, len(fastest_path), 6):
        answer.append(fastest_path[offset:offset+3])
    answer.append(fastest_path[-3:])

    return answer

print(solution([["ICN", "JFK"], ["HND", "IAD"], ["JFK", "HND"]]))
print(solution([["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL","SFO"], ["SFO", "ICN"]]))
# print(
#     solution(
#         [["ICN", "A"], ["ICN", "B"], ["ICN", "C"], ["A", "AA"], ["A", "BB"]]
#     )
# )