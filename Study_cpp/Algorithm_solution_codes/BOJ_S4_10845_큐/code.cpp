#include <iostream>
#include <string>

using namespace std;

class CustomQueue {
private:
  int s;
  int front;
  int rear;
  int* arr;
public:
  CustomQueue(int _size) {
    s = _size;
    front = 0;
    rear = 0;
    arr = new int[s];
  }
  ~CustomQueue() {
    delete[] arr;
  }
  void push(int x) {
    arr[rear] = x;
    rear++;
  }
  int pop() {
    if (front == rear) return -1;
    int ret = arr[front];
    front++;
    return ret;
  }
  int size() {
    return rear - front;
  }
  bool empty() {
    return front == rear;
  }
  int f() {
    if (empty()) return -1;
    else return arr[front];
  }
  int back() {
    if (empty()) return -1;
    else return arr[rear - 1];
  }
};

int main() {
  int N;
  cin >> N;
  string ret = "";
  CustomQueue s(N);
  for (int _ = 0; _ < N; _++) {
    string order;
    cin >> order;

    if (order == "push") {
      int data;
      cin >> data;
      s.push(data);
    }
    else if (order == "pop") {
      ret += to_string(s.pop()) + "\n";
    }
    else if (order == "size") {
      ret += to_string(s.size()) + "\n";
    }
    else if (order == "empty") {
      ret += to_string(s.empty()) + "\n";
    }
    else if (order == "front") {
      ret += to_string(s.f()) + "\n";
    }
    else if (order == "back") {
      ret += to_string(s.back()) + "\n";
    }
  }
  cout << ret << endl;
}