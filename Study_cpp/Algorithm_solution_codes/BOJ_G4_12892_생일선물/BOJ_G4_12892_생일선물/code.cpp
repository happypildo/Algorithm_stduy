#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool debug = true;

struct Present {
	int price;
	int value;

	Present(int _price, int _value) {
		price = _price;
		value = _value;
	}
	/*bool operator < (const Present& other) const {
		if (value < other.value) return true;
		else if (value > other.value) return false;
		if (price > other.price) return true;
		return false;
	}*/
};

bool compare(Present& a, Present& b) {
	if (a.value > b.value) return true;
	else if (a.value < b.value) return false;
	if (a.price < b.price) return true;
	return false;
}

int main() {
	int N, D;
	cin >> N >> D;

	vector<Present> presents;

	for (int i = 0; i < N; i++) {
		int p, v;
		cin >> p >> v;
		presents.push_back(Present(p, v));
	}
	sort(presents.begin(), presents.end(), compare);
	if (debug) {
		for (int i = 0; i < N; i++) {
			cout << "(" << presents[i].value << ", " << presents[i].price << ") ";
		}
		cout << endl;
	}
}