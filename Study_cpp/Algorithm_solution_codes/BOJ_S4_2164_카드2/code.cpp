#include <iostream>

using namespace std;

struct Node {
  int data;
  Node* left;
  Node* right;

  Node(int _data) {
    data = _data;
    left = nullptr;
    right = nullptr;
  }
};

class LinkedList {
private:
  int size;
  Node* head;
  Node* tail;
public:
  LinkedList(int _size) {
    size = _size;
    head = new Node(0);
    tail = new Node(0);

    head->right = tail;
    tail->left = head;
  }
  ~LinkedList() {
      while (head) {
          Node* temp = head;
          head = head->right;
          delete temp;
      }
  }
  void monitor() {
    Node* curr = head->right;
    cout << "[LinkedList]" << endl;
    while (curr != tail) {
      cout << curr->data << "\t";
      curr = curr->right;
    }
    cout << endl;
  }
  void initialize() {
    for (int i = 0; i < size; i++) {
      Node* new_node = new Node(i + 1);
      Node* temp_node = tail->left;

      new_node->right = tail;
      tail->left = new_node;
      temp_node->right = new_node;
      new_node->left = temp_node;
    }
  }
  int shuffling() {
    while (size > 1) {
      // 맨 앞 카드 삭제
      Node* to_be_deleted = head->right;

      head->right = to_be_deleted->right;
      to_be_deleted->right->left = head;

      delete to_be_deleted;
      size--;

      // 그 다음 카드 맨 아래로 이동
      Node* target_node = head->right;
      
      // target node 삭제
      head->right = target_node->right;
      target_node->right->left = head;

      // target node 맨 아래로 이동
      Node* temp_node = tail->left;
      temp_node->right = target_node;
      target_node->left =  temp_node;
      target_node->right = tail;
      tail->left = target_node;

      if(size == 1) return head->right->data;
      // monitor();
    }

    return head->right->data;
  }
};

int main() {
  int N = 0;
  cin >> N;

  LinkedList ll(N);
  ll.initialize();
  // ll.monitor();

  cout << ll.shuffling() << endl;
}