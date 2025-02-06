#include <iostream>
#include <vector>

using namespace std;

int ride_ladder(int N, int H, vector<vector<bool>>& ladder) {
	int wrong_count = 0;
	for (int start = 0; start < N; start++) {
		int width = start;
		int height = 0;

		while (height < H) {
			if (ladder[height][width]) width++;
			else if (width > 0 && ladder[height][width - 1]) width--;
			height++;
		}

		if (width != start) wrong_count++;
	}
	return wrong_count;
}

int min_value = 4;
void find_optimal(int N, int H, int start, vector<vector<bool>>& ladder, vector<pair<int, int>>& selected) {
	int wrong_count = ride_ladder(N, H, ladder);
	if (min_value <= selected.size() + (int)(wrong_count / 2)) return;
	if (wrong_count == 0) min_value = (min_value > selected.size() ? selected.size() : min_value);
	if (selected.size() >= min_value) return;
	if (selected.size() == 4) return;

	for (int idx = start; idx < N * H; idx++) {
		int i = (int)(idx/ N);
		int j = idx - i * N;

		if (ladder[i][j]) continue;
		else if (j == N - 1) continue;
		else if (j > 0 && ladder[i][j - 1]) continue;
		else if (j < N - 1 && ladder[i][j + 1]) continue;

		ladder[i][j] = true;
		selected.push_back(make_pair(i, j));

		find_optimal(N, H, idx + 1, ladder, selected);

		ladder[i][j] = false;
		selected.pop_back();
	}
}

int main() {
	int N, M, H;

	cin >> N >> M >> H;

	vector<vector<bool>> ladder(H, vector<bool>(N, false));
	for (int i = 0; i < M; i++) {
		int a = -1, b = -1;
		cin >> a >> b;

		ladder[a - 1][b - 1] = true;
	}

	vector<pair<int, int>> selected;

	ride_ladder(N, H, ladder);
	find_optimal(N, H, 0, ladder, selected);

	if (min_value >= 4) min_value = -1;
	cout << min_value << endl;
}