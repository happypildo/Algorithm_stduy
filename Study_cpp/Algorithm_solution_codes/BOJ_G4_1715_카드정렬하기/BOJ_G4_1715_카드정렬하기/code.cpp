#include <iostream>
#include <queue>
#include <vector>

using namespace std;

int main() {
	int N;
	cin >> N;

	priority_queue<int> pq;

	for (int i = 0; i < N; i++) {
		int val;
		cin >> val;
		pq.push(-1 * val);
	}

	int ret = 0;
	while (!pq.empty()) {
		int a = pq.top();
		pq.pop();
		if (pq.empty()) {
			break;
		}
		int b = pq.top();
		pq.pop();

		ret += a + b;
		pq.push(a + b);
	}
	cout << -1 * ret << endl;
}