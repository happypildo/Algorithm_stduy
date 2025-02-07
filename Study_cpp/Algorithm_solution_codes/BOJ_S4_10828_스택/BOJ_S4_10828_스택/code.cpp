#include <iostream>
#include <string>

using namespace std;

class CustomStack {
private:
	int size = 10000;
	int rear = 0;
	int* stack;

public:
	CustomStack() {
		stack = new int[size];
	}
	~CustomStack() {
		delete[] stack;
	}
	void push(int x) {
		stack[rear] = x;
		rear++;
	}
	int pop() {
		if (rear == 0) return -1;
		int ret = stack[rear - 1];
		rear--;

		return ret;
	}
	int _size() {
		return rear;
	}
	bool empty() {
		return rear == 0;
	}
	int top() {
		if (rear == 0) return -1;
		return stack[rear - 1];
	}
};

int main() {
	int N = 0;
	cin >> N;

	string ret = "";
	CustomStack s;
	for (int i = 0; i < N; i++) {
		string order;
		cin >> order;

		if (order == "push") {
			int value;
			cin >> value;
			s.push(value);
		}
		else if (order == "pop") {
			//cout << s.pop() << endl;
			ret += to_string(s.pop()) + "\n";
		}
		else if (order == "size") {
			//cout << s._size() << endl;
			ret += to_string(s._size()) + "\n";
		}
		else if (order == "empty") {
			//cout << s.empty() << endl;
			ret += to_string(s.empty()) + "\n";
		}
		else {
			//cout << s.top() << endl;
			ret += to_string(s.top()) + "\n";
		}
	}
	cout << ret << endl;
}