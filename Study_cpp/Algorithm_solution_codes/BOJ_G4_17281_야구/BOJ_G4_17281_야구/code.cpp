#include <iostream>
#include <vector>

using namespace std;

int max_value = -1;

int get_result(vector<vector<int>>& orders, vector<int>& players_order) {
	int curr_player_pos = 0;
	int total_point = 0;

	players_order.insert(players_order.begin() + 4, 0);
	for (int inn = 0; inn < orders.size(); inn++) {
		int out_count = 0;
		int point_arr[4] = { 1, 0, 0, 0 };

		while (true) {
			int idx = players_order[curr_player_pos];
			point_arr[0] = 1;
			int order = orders[inn][idx];

			switch (order) {
			case 0:
				out_count++;
				break;
			default:
				for (int i = 3; i > -1; i--) {
					if (i + order > 3) {
						total_point += point_arr[i];
					}
					else {
						point_arr[i + order] = point_arr[i];
					}
					point_arr[i] = 0;
				}
			}
			
			if (out_count == 3) break;
			curr_player_pos++;
			if (curr_player_pos > 8) curr_player_pos = 0;
		}
	}
	players_order.erase(players_order.begin() + 3);

	return total_point;
}

void permutation(vector<vector<int>>& orders, vector<int>& numbers, vector<bool>& is_selected, vector<int>& perm, int depth) {
	if (depth == numbers.size()) {
		//cout << "[permutation]" << endl;
		//for (auto it : perm) {
		//	cout << it << " ";
		//}
		//cout << endl;

		int point = get_result(orders, perm);
		if (max_value < point) max_value = point;

		return;
	}

	for (int i = 0; i < numbers.size(); i++) {
		if (is_selected[i]) continue;
		is_selected[i] = true;
		perm[depth] = numbers[i];
		permutation(orders, numbers, is_selected, perm, depth + 1);
		is_selected[i] = false;
	}
}

int main() {
	int N;
	cin >> N;

	vector<vector<int>> orders(N);
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < 9; j++) {
			int o;
			cin >> o;
			orders[i].push_back(o);
		}
	}

	vector<int> numbers;
	for (int i = 0; i < 8; i++) numbers.push_back(i + 1);
	vector<bool> is_selected(8, false);
	vector<int> perm(8, -1);
	permutation(orders, numbers, is_selected, perm, 0);

	cout << max_value << endl;
}