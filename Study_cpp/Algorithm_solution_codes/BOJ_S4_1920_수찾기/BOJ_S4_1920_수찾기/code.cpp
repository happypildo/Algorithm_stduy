#include <iostream>

using namespace std;

void swap(int a, int b, long* arr) {
	int temp = arr[a];
	arr[a] = arr[b];
	arr[b] = temp;
}

void quick_sort(int start, int end, long* arr) {
	if (start >= end) return;
	int pivot = start;
	int front = start + 1;
	int rear = end;

	while (front <= rear) {
		bool f = arr[pivot] >= arr[front];
		bool r = arr[pivot] <= arr[rear];
		if (f && r) {
			front++;
			rear--;
		} 
		else if (!f && !r) {
			swap(front, rear, arr);
			front++;
			rear--;
		}
		else if (f) {
			front++;
		}
		else if (r) {
			rear--;
		}
	}
	swap(pivot, rear, arr);

	//cout << "[Quick Sort] " << start << " " << end << endl;
	//for (int i = 0; i < 10; i++) {
	//	cout << arr[i] << "\t";
	//}
	//cout << endl;

	quick_sort(start, rear - 1, arr);
	quick_sort(rear + 1, end, arr);
}

bool binary_search(int start, int end, int N, long target, long* arr) {
	if (start == end) {
		return target == arr[start];
	}
	if (start > end) {
		return false;
	}

	int mid = (int)((start + end) / 2);
	if (target < arr[mid]) {
		return binary_search(start, mid - 1, N, target, arr);
	}
	else if (target == arr[mid]) return true;
	else {
		return binary_search(mid + 1, end, N, target, arr);
	}
}

int main() {
	int N;
	cin >> N;

	long* arr = new long[N];
	for (int i = 0; i < N; i++) {
		cin >> arr[i];
	}

	quick_sort(0, N - 1, arr);

	int M;
	cin >> M;

	for (int i = 0; i < M; i++) {
		long target = 0;
		cin >> target;
		cout << binary_search(0, N, N, target, arr) << endl;
	}

	delete[] arr;
}