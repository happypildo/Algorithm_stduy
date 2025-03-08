#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int max_dist = 999999999;
int dist_arr[3] = {1, 1, 0};
struct node {
    int node_num;
    int dist;

    node(int _node_num, int _dist) {
        node_num = _node_num;
        dist = _dist;
    }

    bool operator < (const node& other) const {
        return dist > other.dist;
    }
};

int main() {
    int N, K;
    cin >> N >> K;

    if (N >= K) {
        cout << N - K << endl;
        return 0;
    }

    vector<int> distance_map(200001, max_dist);
    distance_map[N] = 0;

    // dijkstra
    node curr_node(N, 0);
    priority_queue<node> pq;
    pq.push(curr_node);

    while (!pq.empty()) {
        node curr_node = pq.top();
        pq.pop();

        for (int i = 0; i < 3; i++) {
            // if (i == 2 && double(K) <= (3. / 2.) * double(curr_node.node_num)) continue;
            if (i == 2 && 2 * curr_node.node_num > 100001) continue;
            
            int next_node_num = curr_node.node_num;
            if (i == 0) next_node_num -= 1;
            else if (i == 1) next_node_num += 1;
            else next_node_num *= 2;

            int cost = max_dist;
            if (i == 0 && next_node_num > -1) cost = 1;
            else if (i == 1 && next_node_num < 200001) cost = 1;
            else if (i == 2 && next_node_num < 200001) cost = 0;
            if (cost == max_dist) continue;

            if (curr_node.dist + cost < distance_map[next_node_num]) {
                distance_map[next_node_num] = curr_node.dist + cost;
                pq.push(node(next_node_num, distance_map[next_node_num]));
            }
        }
    }

    cout << distance_map[K] << endl;

    return 0;
}   