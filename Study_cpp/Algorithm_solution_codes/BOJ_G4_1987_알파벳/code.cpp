#include <iostream>
#include <string>

using namespace std;

int max_len = -1;
int DIRECTION[4][2] = {
    {-1, 0}, {1, 0}, {0, -1}, {0, 1}
};

void DFS(char** maze, int R, int C, bool* is_visited_alpha, int x, int y, int depth) {
    for (int d = 0; d < 4; d++) {
        int temp_x = x + DIRECTION[d][0];
        int temp_y = y + DIRECTION[d][1];

        if (-1 < temp_x && temp_x < R && -1 < temp_y && temp_y < C) {
            char next = maze[temp_x][temp_y];
            if (is_visited_alpha[(int)next - 65]) continue;
            is_visited_alpha[(int)next - 65] = true;
            DFS(maze, R, C, is_visited_alpha, temp_x, temp_y, depth + 1);
            is_visited_alpha[(int)next - 65] = false;
        }
    }

    if (max_len < depth) max_len = depth;
}

int main() {
    int R, C;
    cin >> R >> C;

    char** maze = new char*[R];
    for (int i = 0; i < R; i++) {
        maze[i] = new char[C];

        string line;
        cin >> line;
        for (int j = 0; j < line.size(); j++) {
            maze[i][j] = line[j];
        }
    }

    bool is_visited_alpha[26];
    for (int i = 0; i < 26; i++) is_visited_alpha[i] = false;

    is_visited_alpha[(int)maze[0][0] - 65] = true;
    DFS(maze, R, C, is_visited_alpha, 0, 0, 0);

    cout << max_len + 1 << endl;

    for (int i = 0; i < R; i++) {
        delete[] maze[i];
    }
    delete[] maze;
}