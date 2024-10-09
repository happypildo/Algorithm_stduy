class Tagger:
    tagger_direction = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    reverse_direction_idx = [2, 1, 0, 3]
    def __init__(self, map_size):
        self.map_size = map_size
        self.move_direction = []

        cnt = 1
        moving_dist = 1
        repeat_cnt = []
        while moving_dist < self.map_size:
            if cnt < 3:
                repeat_cnt.append(moving_dist)
            else:
                moving_dist += 1
                cnt = 0
            cnt += 1
        repeat_cnt.append(repeat_cnt[-1])

        move_dir = 0
        for r_cnt in repeat_cnt:
            for _ in range(r_cnt):
                self.move_direction.append(Tagger.tagger_direction[move_dir])
            move_dir += 1
            if move_dir == len(Tagger.tagger_direction):
                move_dir = 0

        move_dir = 0
        for r_cnt in repeat_cnt[::-1]:
            for _ in range(r_cnt):
                self.move_direction.append(Tagger.tagger_direction[Tagger.reverse_direction_idx[move_dir]])
            move_dir += 1
            if move_dir == len(Tagger.tagger_direction):
                move_dir = 0

        self.x, self.y = self.map_size // 2, self.map_size // 2
        self.facing = self.move_direction[0]

    def move(self, tik):
        tik = tik % len(self.move_direction)

        dx, dy = self.move_direction[tik]
        self.facing = self.move_direction[(tik + 1) % len(self.move_direction)]
        self.x, self.y = self.x + dx, self.y + dy

    def tag(self):
        tagging_area = [(self.x, self.y)]

        for i in range(2):
            temp_x, temp_y = tagging_area[-1]
            temp_x, temp_y = temp_x + self.facing[0], temp_y + self.facing[1]

            if (-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size):
                tagging_area.append((temp_x, temp_y))

        return tagging_area


class Player:
    DIRECTION = [[-1, 0], [0, -1], [1, 0], [0, 1]]

    def __init__(self, map_size, x, y, d):
        self.map_size = map_size

        if d == 1:
            self.direction = 3
        else:
            self.direction = 2

        self.x = x - 1
        self.y = y - 1
        self.is_survived = True

    def move(self, loc_of_tag):
        if abs(self.x - loc_of_tag[0]) + abs(self.y - loc_of_tag[1]) > 3:
            return False

        temp_x, temp_y = self.x + Player.DIRECTION[self.direction][0], self.y + Player.DIRECTION[self.direction][1]

        if (-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size):
            if (temp_x, temp_y) == loc_of_tag:
                return False
            else:
                self.x, self.y = temp_x, temp_y
        else:
            self.direction = (self.direction + 2) % len(Player.DIRECTION)

            temp_x, temp_y = self.x + Player.DIRECTION[self.direction][0], self.y + Player.DIRECTION[self.direction][1]

            if (temp_x, temp_y) == loc_of_tag:
                return False
            else:
                self.x, self.y = temp_x, temp_y

        return True


class Game:
    def __init__(self, map_size, num_of_trees, num_of_players, tik):
        self.map_size = map_size
        self.num_of_trees = num_of_trees
        self.num_of_players = num_of_players
        self.play_times = tik

        self.tagger = Tagger(self.map_size)
        self.players = []
        self.trees = set()

        self.score = 0

    def initialize(self, player_info, tree_info):
        for info in player_info:
            self.players.append(Player(self.map_size, *info))
        for info in tree_info:
            self.trees.add((info[0] - 1, info[1] - 1))

    def play_game(self):
        for tik in range(self.play_times):
            player_loc = [[[] for _ in range(self.map_size)] for _ in range(self.map_size)]
            for player in self.players:
                if player.is_survived:
                    player.move((self.tagger.x, self.tagger.y))
                    player_loc[player.x][player.y].append(player)

            self.tagger.move(tik)
            tagging_area = self.tagger.tag()

            num_of_tagged = 0
            for x, y in tagging_area:
                if (x, y) in self.trees:
                    # 나무가 있기에 무시한다.
                    continue
                if len(player_loc[x][y]) != 0:
                    # 여기 사람 있어요
                    num_of_tagged += len(player_loc[x][y])
                    for player in player_loc[x][y]:
                        player.is_survived = False

            self.score += (tik + 1) * num_of_tagged

        return self.score


n, m, h, k = list(map(int, input().split()))
p_info = [list(map(int, input().split())) for _ in range(m)]
t_info = [list(map(int, input().split())) for _ in range(h)]

game = Game(n, h, m, k)
game.initialize(p_info, t_info)
print(game.play_game())
