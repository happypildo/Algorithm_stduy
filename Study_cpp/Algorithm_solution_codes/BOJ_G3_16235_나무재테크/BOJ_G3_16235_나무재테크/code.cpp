#include <iostream>
#include <deque>
#include <vector>
#include <algorithm>

using namespace std;

int DIRECTION[8][2] = {
	{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}
};

struct tree {
	int x;
	int y;
	int age;
	bool is_alive;

	tree(int _x, int _y, int _age) {
		x = _x;
		y = _y;
		age = _age;
		is_alive = true;
	}
};

//bool compare(tree& t1, tree& t2) {
//	return t1.age < t2.age;
//}

vector<deque<tree>> eat(int N, int** land, vector<deque<tree>>& trees) {
	vector<deque<tree>> dead_trees(N * N);

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			// dead_tree_idx 계산이 잘 못 되고 있음...
			int dead_tree_idx = 0;
			for (auto it = trees[i * N + j].begin(); it != trees[i * N + j].end(); it++) {
				int remains = land[i][j] - it->age;
				if (remains < 0) {
					break;
				}
				else {
					land[i][j] = remains;
					it->age++;
				}
				dead_tree_idx++;
			}
			// 나무 죽이는 부분 코드 작성해야 함
			//cout << "[spring] " << i << " " << j << endl;
			//cout << "Tree size: " << trees[i * N + j].size() << " / dead_tree_idx: " << dead_tree_idx << endl;
			int s = trees[i * N + j].size();
			for (int temp = dead_tree_idx; temp < s; temp++) {
				dead_trees[i * N + j].push_back(trees[i * N + j].back());
				trees[i * N + j].pop_back();
			}

		}
	}

	return dead_trees;
}

void neutrionization(int N, int** land, vector<deque<tree>>& dead_trees) {
	//cout << "Neutrionization" << endl;
	for (auto dead_tree : dead_trees) {
		for (auto t : dead_tree) {
			land[t.x][t.y] += (int)(t.age / 2);
		}
	}
}

void autumn_winter(int N, int** land, int** original_land, vector<deque<tree>>& trees) {
	//cout << "autumn_winter" << endl;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			for (auto it = trees[i * N + j].begin(); it != trees[i * N + j].end(); it++) {
				if (it->age % 5 == 0) {
					for (int d = 0; d < 8; d++) {
						int temp_x = i + DIRECTION[d][0];
						int temp_y = j + DIRECTION[d][1];

						if (-1 < temp_x && temp_x < N && -1 < temp_y && temp_y < N) {
							trees[temp_x * N + temp_y].push_front(tree(temp_x, temp_y, 1));
						}

						//cout << "\t" << i << " " << j << " / " << DIRECTION[d][0] << " " << DIRECTION[d][1] << " / " << temp_x << " " << temp_y << endl;
					}
				}
			}

			land[i][j] += original_land[i][j];
		}
	}

	//cout << "[autumn_winter] " << endl;
	//for (int i = 0; i < N; i++) {
	//	for (int j = 0; j < N; j++) {
	//		cout << land[i][j] << "\t";
	//	}
	//	cout << endl;
	//}
	//cout << "Num of trees" << endl;
	//for (int i = 0; i < N; i++) {
	//	for (int j = 0; j < N; j++) {
	//		cout << trees[i * N + j].size() << "\t";
	//	}
	//	cout << endl;
	//}
	//cout << endl;
}

//void winter(int N, int** land, int** original_land) {
//
//}

int main() {
	int N, M, K;

	cin >> N >> M >> K;

	int** land = new int* [N];
	int** original_land = new int* [N];
	for (int i = 0; i < N; i++) {
		land[i] = new int[N];
		original_land[i] = new int[N];

		for (int j = 0; j < N; j++) {
			cin >> original_land[i][j];
			land[i][j] = 5;
		}
	}
	
	vector<deque<tree>> trees(N * N);
	for (int i = 0; i < M; i++) {
		int x, y, age;
		cin >> x >> y >> age;
		x--;
		y--;
		trees[x * N + y].push_back(tree(x, y, age));
	}
	/*for (auto it = trees.begin(); it != trees.end(); it++) {
		sort(it->begin(), it->end(), compare);
	}*/
	
	for (int k = 0; k < K; k++) {
		vector<deque<tree>> dead_trees = eat(N, land, trees);
		neutrionization(N, land, dead_trees);
		autumn_winter(N, land, original_land, trees);
	}

	int answer = 0;
	for (auto t: trees) {
		answer += t.size();
	}
	cout << answer << endl;

	for (int i = 0; i < N; i++) {
		delete[] land[i];
		delete[] original_land[i];
	}
	delete[] land;
	delete[] original_land;
}