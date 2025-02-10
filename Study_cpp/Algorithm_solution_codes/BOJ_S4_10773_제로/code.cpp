#include <iostream>

using namespace std;

class CustomStack {
private:
  int rear;
  int arr[100000];

public:
  CustomStack() {rear = 0;};
  void insert(int x) {
    arr[rear] = x;
    rear++;
  }
  void pop() {
    rear--;
  }
  int result() {
    int ret = 0;
    for (int i = 0; i < rear; i++) {
      ret += arr[i];
    }
    return ret;
  }
};

int main() {
  int N;
  cin >> N;

  CustomStack s;
  for (int i = 0; i < N; i++) {
    int data;
    cin >> data;

    if (data == 0) s.pop();
    else s.insert(data); 
  }
  cout << s.result() << endl;
}