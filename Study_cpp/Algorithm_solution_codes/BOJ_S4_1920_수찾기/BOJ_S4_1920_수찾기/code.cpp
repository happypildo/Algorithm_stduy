#include <iostream>
#include <string>

using namespace std;

class HashTable {
private:
	int size = 100003;
	int modular_value = 100003;
	int** table;
	bool** is_linked;
	int chain_size = 5;

public:
	HashTable() {
		table = new int* [size];
		is_linked = new bool* [size];
		for (int i = 0; i < size; i++) {
			table[i] = new int[chain_size];
			is_linked[i] = new bool[chain_size];
			for (int j = 0; j < chain_size; j++) {
				is_linked[i][j] = false;
			}
		}
	}
	~HashTable() {
		for (int i = 0; i < size; i++) {
			delete[] table[i];
			delete[] is_linked[i];
		}
		//delete[] table;
		//delete[] is_linked;
	}
	void insert(int x) {
		int hash_value = (x % modular_value + modular_value) % modular_value;

		//cout << "[HashTable - insert]" << endl;
		//cout << "called" << endl;
		bool inserted = true;
		while (inserted) {
			for (int i = 0; i < chain_size; i++) {
				if (is_linked[hash_value][i] && x == table[hash_value][i]) return;
				else if (is_linked[hash_value][i]) continue;
				else {
					inserted = false;
					is_linked[hash_value][i] = true;
					table[hash_value][i] = x;
					break;
				}
			}
			hash_value++;
			if (hash_value > size - 1) hash_value = 0;
		}
		//cout << "Over" << endl;
	}
	bool is_in(int x) {
		int hash_value = (x % modular_value + modular_value) % modular_value;
		int original_hash_value = hash_value;
		while (true) {
			for (int i = 0; i < chain_size; i++) {
				if (is_linked[hash_value][i] && table[hash_value][i] == x) return true;
				else if (!is_linked[hash_value][i]) return false;
			}
			hash_value++;
			if (hash_value > size - 1) hash_value = 0;

			if (hash_value == original_hash_value) return false;
		}

		return false;
	}
};

int main() {
	HashTable hash_table;

	int N = 0;
	cin >> N;

	for (int i = 0; i < N; i++) {
		int x = 0;
		cin >> x;
		hash_table.insert(x);
	}

	int M = 0;
	cin >> M;
	string ret = "";
	for (int i = 0; i < M; i++) {
		int x = 0;
		cin >> x;
		if (hash_table.is_in(x)) ret += "1\n";
		else ret += "0\n";
	}

	cout << ret << endl;
}