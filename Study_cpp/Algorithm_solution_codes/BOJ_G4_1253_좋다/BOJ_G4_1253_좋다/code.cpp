#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool is_there(int N, vector<int>& arr, int s, int e, int except, int target) {
	if (s > e) return false;
	if (arr[s] == target) {
		if (s == except) {
			if (s - 1 > -1 && arr[s - 1] == target) return true;
			else if (s + 1 < N && arr[s + 1] == target) return true;
			return false;
		}
		else return true;
	}
	if (arr[e] == target) {
		if (e == except) {
			if (e - 1 > -1 && arr[e - 1] == target) return true;
			else if (e + 1 < N && arr[e + 1] == target) return true;
			return false;
		}
		else return true;
	}

	int middle = (int)((s + e) / 2);

	if (arr[middle] < target) {
		return is_there(N, arr, middle + 1, e, except, target);
	}
	else if (arr[middle] > target) {
		return is_there(N, arr, s + 1, middle - 1, except, target);
	}
	else {
		return true;
	}
}

int main() {
	// 1. Input
	int N;
	cin >> N;

	vector<int> arr(N, 0);

	for (int i = 0; i < N; i++) {
		int val;
		cin >> val;
		arr[i] = val;
	}

	// 2. Sorting
	sort(arr.begin(), arr.end());

	// 3. Binary search
	int num_of_good_value = 0;
	for (int i = 0; i < N; i++) {
		for (int j = 0; j < N; j++) {
			if (i == j) continue;
			int target = arr[i] - arr[j];

			if (arr[i] == arr[j]) {
				if (i + 1 < N - 1 && arr[i] == arr[i + 1]) {
					num_of_good_value++;
					break;
				}
				else if (j - 1 > -1 && arr[j] == arr[j - 1]) {
					num_of_good_value++;
					break;
				}
			}
			else if (is_there(N, arr, j + 1, N - 1, i, target)) {
				num_of_good_value++;
				break;
			}
		}
	}

	cout << num_of_good_value << endl;

	return 0;
}