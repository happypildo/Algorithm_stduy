#include <iostream>
#include <string>

using namespace std;

class ACLanguage {
private:
  int front;
  int rear;
  int is_reversed;
  int* arr;
  int arr_len;
public:
  ACLanguage(int N) {
    arr_len = N;
    arr = new int[arr_len];
    front = 0;
    rear = arr_len - 1;
    is_reversed = 1;
  }
  ~ACLanguage() {
    delete[] arr;
  }
  void initialize(string line) {
    int idx = 0;
    string num = "";
    for (char c : line) {
      if (idx > arr_len - 1) break;
      if (c == '[') continue;

      if (c == ',' || c == ']') {
        arr[idx] = stoi(num);
        num = "";
        idx++;
      }
      else {
        num += c;
      }
    }
  }
  void flip() {
    int temp = rear;
    rear = front;
    front = temp;

    is_reversed *= -1;
  }
  bool drop() {
    if (is_reversed == 1 && front > rear) return false;
    else if (is_reversed == -1 && front < rear) return false;

    front += is_reversed;

    return true;
  }
  string result() {
    string ret = "[";

    for (int i = front; i != rear + is_reversed; i += is_reversed) {
      if (i == rear) ret += to_string(arr[i]) + "]";
      else ret += to_string(arr[i]) + ",";
    }
    if (ret == "[") ret = "[]";
    return ret;
  }
  void monitor() {
    cout << "[ACLanguage]" << endl;
    cout << "front: " << front << endl;
    cout << "rear: " << rear << endl;
    cout << "is_reversed: " << is_reversed << endl;
    for (int i = front; i != rear + is_reversed; i += is_reversed) {
      cout << arr[i] << "\t" ;
    }
    cout << endl;
  }
};

int main() {
  int T = 0;
  cin >> T;

  for (int _ = 0; _ < T; _++) {
    string order;
    cin >> order;

    int N;
    cin >> N;
    ACLanguage ac(N);

    string line;
    cin >> line;
    ac.initialize(line);

    string ret =  "";
    for (char c : order) {
      if (c == 'R') {
        ac.flip();
      }
      else {
        bool jud = ac.drop();
        if (!jud) {
          ret = "error";
          break;
        }
      }
      // ac.monitor();
    }

    if (ret == "error") cout << ret << endl;
    else cout << ac.result() << endl;
  }
}