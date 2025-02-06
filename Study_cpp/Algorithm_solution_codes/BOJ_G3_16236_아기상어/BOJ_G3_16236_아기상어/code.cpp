#include <iostream>
#include <vector>
#include <queue>

using namespace std;

struct Shark {
	int x = 0;
	int y = 0;
	int s_size = 0;
	int size_up_stack = 0;

	Shark() : x(0), y(0), s_size(2), size_up_stack(2) {}
	Shark(int _x, int _y)
		: x(_x), y(_y), s_size(2), size_up_stack(2) {
	}
	void check_size_up() {
		//cout << "[Shark]" << endl;
		//cout << "I ate!! " << size_up_stack << " / " << s_size << endl;
		size_up_stack--;

		if (size_up_stack == 0) {
			s_size++;
			size_up_stack = s_size;
		}
	}
};

struct Node {
	int x;
	int y;
	int cost;

	Node(int _x, int _y, int _cost) {
		x = _x;
		y = _y;
		cost = _cost;
	}

	bool operator < (const Node& other) const {
		return cost > other.cost;
	}
};

struct Feed {
	int x;
	int y;
	int dist;

	Feed(int _x, int _y, int _dist) {
		x = _x;
		y = _y;
		dist = _dist;
	}

	bool operator < (const Feed& other) const {
		if (dist > other.dist) return true;
		else return false;
		if (x > other.x) return true;
		else return false;
		if (y > other.y) return true;
		else return false;
	}
};

int DIRECTION[4][2] = {
	{-1, 0}, {1, 0}, {0, -1}, {0, 1}
};

priority_queue<Feed> dijkstra(int N, vector<vector<int>>& sea, Shark& shark) {
	vector<vector<int>> distance_map(N, vector<int>(N, 999999));
	distance_map[shark.x][shark.y] = 0;
	priority_queue<Node> pq;
	pq.push(Node(shark.x, shark.y, 0));

	while (!pq.empty()) {
		Node node = pq.top();
		pq.pop();

		for (int d = 0; d < 4; d++) {
			int temp_x = node.x + DIRECTION[d][0];
			int temp_y = node.y + DIRECTION[d][1];

			if (-1 < temp_x && temp_x < N && -1 < temp_y && temp_y < N) {
				if (sea[temp_x][temp_y] > shark.s_size) continue;

				if (distance_map[temp_x][temp_y] > distance_map[node.x][node.y] + 1) {
					distance_map[temp_x][temp_y] = distance_map[node.x][node.y] + 1;
					pq.push(Node(temp_x, temp_y, distance_map[temp_x][temp_y]));
				}
			}
		}
	}

	//std::cout << endl;
	//std::cout << "[dijkstra]" << endl;
	//for (int i = 0; i < N; i++) {
	//	for (int j = 0; j < N; j++) {
	//		std::cout << distance_map[i][j] << "\t";
	//	}
	//	std::cout << endl;
	//}

	priority_queue<Feed> feeds;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			if (i == shark.x && j == shark.y) continue;
			if (sea[i][j] >= shark.s_size) continue;
			if (sea[i][j] == 0) continue;
			if (distance_map[i][j] == 999999) continue;
			feeds.push(Feed(i, j, distance_map[i][j]));
		}
	}

	return feeds;
}

int main() {
	int N;
	cin >> N;

	vector<vector<int>> sea(N, vector<int>(N, 0));
	Shark shark(-1, -1);

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			cin >> sea[i][j];
			if (sea[i][j] == 9) {
				sea[i][j] = 0;
				shark = Shark(i, j);
			}
		}
	}

	int answer = 0;
	while (true) {
		priority_queue<Feed> feeds = dijkstra(N, sea, shark);

		if (feeds.size() == 0) break;

		Feed feed = feeds.top();
		shark.check_size_up();
		shark.x = feed.x;
		shark.y = feed.y;
		sea[shark.x][shark.y] = 0;

		answer += feed.dist;
	}

	cout << answer << endl;
}