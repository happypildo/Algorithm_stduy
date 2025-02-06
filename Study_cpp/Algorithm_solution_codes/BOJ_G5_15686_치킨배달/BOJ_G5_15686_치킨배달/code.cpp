#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

void find_via_combination(int& min_dist, int num_of_chicken, int start, vector<bool>& combination, vector<vector<int>>& chck_dist_by_house, int depth, int target_depth) {
	if (target_depth == depth) {
		//cout << "[find_via_combination]" << endl;
		//for (auto it = combination.begin(); it != combination.end(); it++) {
		//	cout << *it;
		//}
		//cout << endl;

		int distance = 0;
		for (auto house = chck_dist_by_house.begin(); house != chck_dist_by_house.end(); house++) {
			int min_dist_of_house = 999999;
			for (int i = 0; i < num_of_chicken; i++) {
				if (!combination[i]) continue;
				int dist = house->at(i);
				min_dist_of_house = (min_dist_of_house < dist ? min_dist_of_house : dist);
			}
			distance += min_dist_of_house;
		}

		min_dist = (min_dist < distance ? min_dist : distance);

		return;
	}

	for (int i = start; i < num_of_chicken; i++) {
		combination[i] = true;
		find_via_combination(min_dist, num_of_chicken, i + 1, combination, chck_dist_by_house, depth + 1, target_depth);
		combination[i] = false;
	}
}

int main() {
	int N, M;

	cin >> N >> M;

	int num_of_house = 0;
	int num_of_chicken = 0;
	vector<pair<int, int>> house_loc;
	vector<pair<int, int>> chicken_loc;

	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			int c = 0;
			cin >> c;
			if (c == 1) {
				num_of_house++;
				house_loc.push_back(make_pair(i, j));
			}
			else if (c == 2) {
				num_of_chicken++;
				chicken_loc.push_back(make_pair(i, j));
			}
		}
	}

	vector<vector<int>> chck_dist_by_house(num_of_house);
	for (int i = 0; i < num_of_house; i++) {
		for (auto it = chicken_loc.begin(); it != chicken_loc.end(); it++) {
			int dist = abs(house_loc[i].first - it->first) + abs(house_loc[i].second - it->second);
			chck_dist_by_house[i].push_back(dist);
		}
	}

	int min_dist = 999999;
	vector<bool> combination(num_of_chicken, false);
	for (int i = 1; i < M + 1; i++){
		find_via_combination(min_dist, num_of_chicken, 0, combination, chck_dist_by_house, 0, i);
	}

	cout << min_dist << endl;
}