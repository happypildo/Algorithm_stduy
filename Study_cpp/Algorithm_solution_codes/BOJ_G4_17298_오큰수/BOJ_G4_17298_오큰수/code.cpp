#include <iostream>
#include <string>

using namespace std;

class PairStack {
private:
	int len;
	int rear;
	pair<int, int>* stack;
public:
	PairStack(int _len) {
		len = _len;
		rear = 0;
		stack = new pair<int, int>[len];
	}
	~PairStack() {
		delete[] stack;
	}
	void push(const pair<int, int>& item) {
		stack[rear] = item;
		rear++;
	}
	bool empty() {
		return rear == 0;
	}
	void pop() {
		if (empty()) return;
		rear--;
	}
	pair<int, int> top() {
		if (empty()) return make_pair(-1, -1);

		pair<int, int> ret = stack[rear - 1];
		return ret;
	}
	
};

int main() {
	int N;
	cin >> N;

	int* NGE = new int[N];
	PairStack stack(N);
	for (int i = 0; i < N; i++) {
		NGE[i] = -1;
		int val;
		cin >> val;

		pair<int, int> item = make_pair(i, val);

		while (!stack.empty()) {
			pair<int, int> popped = stack.top();
			if (popped.second < item.second) {
				stack.pop();
				NGE[popped.first] = item.second;
			}
			else break;
		}
		stack.push(item);
	}

	string ret = "";
	for (int i = 0; i < N; i++) {
		//cout << NGE[i] << " ";
		ret += to_string(NGE[i]) + " ";
	}
	//cout << endl;
	cout << ret << endl;

	delete[] NGE;
}