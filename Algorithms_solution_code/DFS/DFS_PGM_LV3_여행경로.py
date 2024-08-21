# 경로가 유일하지 않은 경우가 있을까?
import copy 
fastest_path = ""
def DFS(source, path_dict, ticket_arr, ticket_dict, travel):
    global fastest_path
    if path_dict.get(source, None) is None:
        # if len(travel) == len(ticket_arr) * 3 * 2:
        if ticket_dict['visited_tickets'] == 0:
            if fastest_path > travel:
                fastest_path = travel
        return
    # if len(travel) == len(ticket_arr) * 3 * 2:
    if ticket_dict['visited_tickets'] == 0:
        if fastest_path > travel:
            fastest_path = travel
        return
    
    if travel > fastest_path:
        return
    
    for destination in path_dict[source]:
        if ticket_dict[(source, destination)] != 0:
            temp_ticket_dict = copy.deepcopy(ticket_dict)
            temp_ticket_dict[(source, destination)] -= 1 
            temp_ticket_dict['visited_tickets'] -= 1

            DFS(destination, path_dict, ticket_arr, temp_ticket_dict, travel + f"{source}{destination}")


def solution(tickets):
    global fastest_path

    path_dict = {}
    ticket_arr = []
    ticket_dict = {}
    for source, destination in tickets:
        ticket_arr.append((source, destination))

        if ticket_dict.get((source, destination), None) is None:
            ticket_dict[(source, destination)] = 1
        else:
            ticket_dict[(source, destination)] += 1
        if path_dict.get(source, None) is None:
            path_dict[source] = [destination]
        else:
            path_dict[source].append(destination)
    ticket_dict["num_of_tickets"] = len(tickets)
    ticket_dict["visited_tickets"] = len(tickets)

    fastest_path = "a" * ticket_dict["num_of_tickets"] * 3 * 2
    DFS(source="ICN", path_dict=path_dict, ticket_arr=ticket_arr, ticket_dict=ticket_dict, travel="")
    
    # PROCESSING
    answer = []
    for offset in range(0, len(fastest_path), 6):
        answer.append(fastest_path[offset:offset+3])
    answer.append(fastest_path[-3:])

    return answer

print(solution([["ICN", "JFK"], ["HND", "IAD"], ["JFK", "HND"]]))
print(solution([["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL","SFO"], ["SFO", "ICN"]]))
print(solution([["ICN", "SFO"], ["SFO", "ICN"], ["ICN", "SFO"], ["SFO", "ICN"]]))
# print(
#     solution(
#         [["ICN", "A"], ["ICN", "B"], ["ICN", "C"], ["A", "AA"], ["A", "BB"]]
#     )
# )