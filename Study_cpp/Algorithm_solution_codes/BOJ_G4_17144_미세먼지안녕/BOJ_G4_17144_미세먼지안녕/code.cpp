#include <iostream>
#include <vector>
#include <deque>

using namespace std;

int DIRECTION[4][2] = {
	{-1, 0}, {1, 0}, {0, -1}, {0, 1}
};

vector<vector<int>> spread(int R, int C, vector<vector<int>>& room) {
	vector<vector<int>> new_room(R, vector<int>(C, 0));

	for (int i = 0; i < R; i++) {
		for (int j = 0; j < C; j++) {
			if (room[i][j] > 0) {
				// 미세 먼지가 있는 곳
				int num_of_spread = 0;
				for (int d = 0; d < 4; d++) {
					int temp_x = i + DIRECTION[d][0];
					int temp_y = j + DIRECTION[d][1];

					if (0 > temp_x || R - 1 < temp_x || 0 > temp_y || C - 1 < temp_y) continue;
					if (room[temp_x][temp_y] == -1) continue;

					new_room[temp_x][temp_y] += (int)(room[i][j] / 5);
					num_of_spread++;
				}
				new_room[i][j] += room[i][j] - (int)(room[i][j] / 5) * num_of_spread;
			}
		}
	}

	return new_room;
}

int main() {
	int R, C, T;
	cin >> R >> C >> T;

	vector<vector<int>> room(R, vector<int>(C, 0));
	vector<vector<pair<int, int>>> purifier(2);

	int is_upper = 0;
	int sequence[4] = { 3, 0, 2, 1 };
	for (int i = 0; i < R; i++) {
		for (int j = 0; j < C; j++) {
			cin >> room[i][j];
			if (room[i][j] == -1) {
				// something
				purifier[is_upper].push_back(make_pair(i, j + 1));
				for (int s = 0; s < 4; s++) {
					while (true) {
						int temp_x = purifier[is_upper].back().first + DIRECTION[sequence[s]][0];
						int temp_y = purifier[is_upper].back().second + DIRECTION[sequence[s]][1];
						if (-1 < temp_x && temp_x < R && -1 < temp_y && temp_y < C) {
							purifier[is_upper].push_back(make_pair(temp_x, temp_y));
							if (i == temp_x && j == temp_y) break;
						}
						else break;
					}
				}
				is_upper++;
				sequence[1] = 1;
				sequence[3] = 0;

			}
		}
	}

	for (int t = 0; t < T; t++) {
		room = spread(R, C, room);

		for (int p = 0; p < 2; p++) {
			deque<int> tickles;
			for (auto it = purifier[p].begin(); it != purifier[p].end(); it++) {
				tickles.push_back(room[it->first][it->second]);
			}
			tickles.push_front(0);
			tickles.pop_back();
			for (int i = 0; i < tickles.size(); i++) {
				room[purifier[p][i].first][purifier[p][i].second] = tickles[i];
			}
		}
		room[purifier[0].back().first][purifier[0].back().second] = -1;
		room[purifier[1].back().first][purifier[1].back().second] = -1;
	}

	int answer = 0;
	for (int i = 0; i < R; i++) {
		for (int j = 0; j < C; j++) {
			answer += room[i][j];
		}
	}
	answer += 2;
	cout << answer << endl;
}