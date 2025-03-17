#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
bool debug = false;


int main() {
	int N;
	cin >> N;

	vector<int> arr(N, 0);
	for (int i = 0; i < N; i++) {
		cin >> arr[i];
	}
	sort(arr.begin(), arr.end());
	if (debug) {
		for (auto it = arr.begin(); it != arr.end(); it++) {
			cout << *it << " ";
		}
		cout << endl;
	}

	int num_of_good = 0;
	for (int i = 0; i < N; i++) {
		int left = 0;
		int right = N - 1;
		while (left < right) {
			if (left == i) { left++; continue; }
			if (right == i) { right--; continue; }

			int target = arr[left] + arr[right];

			if (target < arr[i]) left++;
			else if (target > arr[i]) right--;
			else { num_of_good++; break; }
		}
	}

	cout << num_of_good << endl;

	return 0;
}