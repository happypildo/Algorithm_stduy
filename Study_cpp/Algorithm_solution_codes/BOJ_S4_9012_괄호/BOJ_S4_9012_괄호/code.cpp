#include <iostream>
#include <string>

using namespace std;

template <typename T>
class Custom_Stack {
private:
	int size;
	T* arr;
	int front = 0;
	int rear = 0;

public:
	Custom_Stack(int _size) {
		size = _size;
		arr = new T[size];
	}
	~Custom_Stack() {
		delete[] arr;
	}
	void monitor() {
		cout << "Stack status" << endl;
		cout << "[size / front / rear]: " << size << " " << front << " " << rear << endl;
	}
	void push(T data) {
		arr[rear] = data;
		rear++;
	}
	T pop() {
		if (rear == 0) return T();
		T data = arr[rear - 1];
		rear--;
		return data;
	}
	bool is_empty() {
		return front == rear;
	}
};

int main() {
	int N;
	cin >> N;

	for (int t = 0; t < N; t++) {
		string answer = "NO";
		string line;
		cin >> line;

		bool is_done = true;
		Custom_Stack<char> s(line.size());
		for (int i = 0; i < line.size(); i++) {
			// Something to do
			if (line[i] == '(') {
				s.push('(');
			}
			else {
				char p = s.pop();

				if (p != '(') {
					is_done = false;
					break;
				}
			}
			//s.monitor();
		}
		if (is_done && s.is_empty()) answer = "YES";

		cout << answer << endl;
	}
}