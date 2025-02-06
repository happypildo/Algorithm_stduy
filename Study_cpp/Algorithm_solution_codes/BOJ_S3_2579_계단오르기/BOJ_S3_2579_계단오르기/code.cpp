#include <iostream>

using namespace std;

int main() {
	int N = 0;
	cin >> N;

	int* stair = new int[N];
	for (int i = 0; i < N; i++) {
		cin >> stair[i];
	}

	if (N == 1) cout << stair[0] << endl;
	else {
		int** DP = new int* [2];
		for (int i = 0; i < 2; i++) {
			DP[i] = new int[N];
		}

		DP[0][0] = stair[0];
		DP[0][1] = stair[0] + stair[1];
		DP[1][1] = stair[1];
		DP[1][0] = -100000;

		for (int i = 2; i < N; i++) {
			DP[0][i] = max(DP[0][i - 2] + stair[i], DP[1][i - 1] + stair[i]);
			DP[1][i] = max(DP[0][i - 2] + stair[i], DP[1][i - 2] + stair[i]);
		}

		cout << max(DP[0][N - 1], DP[1][N - 1]) << endl;

		for (int i = 0; i < 2; i++) {
			delete[] DP[i];
		}
		delete[] DP;
	}
	delete[] stair;
}