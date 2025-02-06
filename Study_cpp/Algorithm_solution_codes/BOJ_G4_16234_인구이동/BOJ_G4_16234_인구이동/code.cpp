#include <iostream>
#include <vector>
#include <cmath>
#include <queue>

using namespace std;

int DIRECTION[4][2] = {
	{-1, 0}, {1, 0}, {0, -1}, {0, 1}
};

vector<vector<int>> link_border(int N, int L, int R, int** world, bool& jud) {
	vector<vector<int>> graph(N * N);

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (int d = 0; d < 4; d++) {
				int temp_x = i + DIRECTION[d][0];
				int temp_y = j + DIRECTION[d][1];

				if (-1 < temp_x && temp_x < N && -1 < temp_y && temp_y < N) {
					int diff = abs(world[i][j] - world[temp_x][temp_y]);
					//cout << "[link border]" << endl;
					//cout << "Link [" << i << " - " << j << "] & [" << temp_x << " - " << temp_y << "] : " << diff << endl;
					if (L <= diff && diff <= R) {
						jud = true;
						graph[i * N + j].push_back(temp_x * N + temp_y);
						graph[temp_x * N + temp_y].push_back(i * N + j);
					}
				}
			}
		}
	}
	
	return graph;
}

void BFS(int N, int** world, vector<vector<int>>& graph, vector<bool> is_visited, int start) {
	queue<int> q;
	q.push(start);

	is_visited[start] = true;
	vector<int> current_visited;
	current_visited.push_back(start);

	int total_population = world[(int)(start / N)][start - (int)(start / N) * N];

	while (!q.empty()) {
		int node = q.front();
		q.pop();

		for (auto neighbor = graph[node].begin(); neighbor != graph[node].end(); neighbor++) {
			if (is_visited[*neighbor]) continue;

			is_visited[*neighbor] = true;
			q.push(*neighbor);
			current_visited.push_back(*neighbor);
			total_population += world[(int)(*neighbor / N)][*neighbor - (int)(*neighbor / N) * N];
		}
	}

	for (auto it = current_visited.begin(); it != current_visited.end(); it++) {
		world[(int)(*it / N)][*it - (int)(*it / N) * N] = (int)total_population / current_visited.size();
	}
}

int main() {
	int N, L, R;
	cin >> N >> L >> R;

	int** world = new int* [N];
	for (int i = 0; i < N; i++) {
		world[i] = new int[N];
		for (int j = 0; j < N; j++) {
			cin >> world[i][j];
		}
	}

	int day_count = 0;
	while (true) {
		bool jud = false;
		vector<vector<int>> graph = link_border(N, L, R, world, jud);
		if (!jud) break;

		vector<bool> is_visited(N * N, false);
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				int start = i * N + j;
				if (is_visited[start]) continue;
				BFS(N, world, graph, is_visited, start);
			}
		}
		day_count++;

		//cout << "[Main]" << endl;
		//for (int i = 0; i < N; i++) {
		//	for (int j = 0; j < N; j++) {
		//		cout << world[i][j] << "\t";
		//	}
		//	cout << endl;
		//}
		//cout << endl;
	}

	for (int i = 0; i < N; i++) {
		delete[] world[i];
	}
	delete[] world;

	cout << day_count << endl;

	return 0;
}