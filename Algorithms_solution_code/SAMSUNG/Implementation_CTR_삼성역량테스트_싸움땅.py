DIRECTION = [
    [-1, 0], [0, 1], [1, 0], [0, -1]
]
REVERSE = {
    0: 2,
    1: 3,
    2: 0,
    3: 1
}

class Player:
    def __init__(self, idx, x, y, d, s):
        self.player_num = idx + 1
        self.x = x
        self.y = y
        self.d = d
        self.s = s

        self.guns = []
        self.points = 0


class Gun:
    def __init__(self, power):
        self.power = power


class Game:
    def __init__(self, map_size, game_map, num_of_players):
        self.map_size = map_size
        self.game_map = game_map
        self.player_move_map = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]
        self.players = [Player(-1, -1, -1, -1, -1) for _ in range(num_of_players)]

    def initialize(self, info):
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.game_map[x][y] = [Gun(self.game_map[x][y])]

        for idx, p_info in enumerate(info):
            self.players[idx] = Player(idx, p_info[0] - 1, p_info[1] - 1, *p_info[2:])
            self.player_move_map[p_info[0] - 1][p_info[1] - 1] = idx + 1

    def move(self, player_idx, ignore_player=False):
        has_to_fight = False

        player = self.players[player_idx]

        x, y = player.x, player.y
        direction = player.d
        temp_x, temp_y = x + DIRECTION[direction][0], y + DIRECTION[direction][1]

        if ignore_player:
            # 앞에 플레이어가 있던 없던 돌진
            if (-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size):
                player.x = temp_x
                player.y = temp_y
                if self.player_move_map[temp_x][temp_y] != 0:
                    # 싸워야 한다.
                    has_to_fight = True
            else:
                player.d = REVERSE[player.d]
                direction = player.d
                temp_x, temp_y = x + DIRECTION[direction][0], y + DIRECTION[direction][1]

                player.x = temp_x
                player.y = temp_y
                if self.player_move_map[temp_x][temp_y] != 0:
                    # 싸워야 한다.
                    has_to_fight = True

            return has_to_fight
        else:
            # 앞에 플레이어가 있다면 빙글빙글
            while True:
                if ((-1 < temp_x < self.map_size) and (-1 < temp_y < self.map_size)) and self.player_move_map[temp_x][temp_y] == 0:
                    # 아무도 없어! 이동하자!
                    player.x = temp_x
                    player.y = temp_y
                    return has_to_fight
                else:
                    # 무엇가 있다. 빙글빙글 돌자.
                    player.d = player.d + 1
                    if player.d == 4:
                        player.d = 0
                    direction = player.d
                    temp_x, temp_y = x + DIRECTION[direction][0], y + DIRECTION[direction][1]

    def players_fight(self, p1, p2):
        p1_power = p1.s + sum([g.power for g in p1.guns])
        p2_power = p2.s + sum([g.power for g in p2.guns])

        if p1_power > p2_power:
            p1.points += p1_power - p2_power
            return True
        elif p1_power < p2_power:
            p2.points += p2_power - p1_power
            return False

        if p1.s > p2.s:
            p1.points += p1_power - p2_power
            return True
        else:
            p2.points += p2_power - p1_power
            return False

    def grab_gun(self, player_idx):
        player = self.players[player_idx]
        guns_on_land = self.game_map[player.x][player.y]

        total = player.guns + guns_on_land
        strong_power = -1
        strong_idx = -1

        if len(total) == 0:
            return

        for idx, gun in enumerate(total):
            if strong_power < gun.power:
                strong_power = gun.power
                strong_idx = idx

        player.guns = [total[strong_idx]]
        self.game_map[player.x][player.y] = total[:strong_idx] + total[strong_idx + 1:]

    def play(self, sim_time):
        for tik in range(sim_time):
            for idx, player in enumerate(self.players):
                self.player_move_map[player.x][player.y] = 0
                has_to_fight = self.move(idx, ignore_player=True)

                if has_to_fight:
                    # 싸워야 한다...
                    opposite_idx = self.player_move_map[player.x][player.y] - 1
                    opposite = self.players[opposite_idx]

                    if self.players_fight(player, opposite):
                        # player 이김 -> opposite은 움직여야 한다. 단, ignore하면 안 된다.
                        self.game_map[opposite.x][opposite.y].extend(opposite.guns[:])
                        opposite.guns = []

                        self.move(opposite_idx, ignore_player=False)
                        self.grab_gun(opposite_idx)

                        self.grab_gun(idx)

                        prev_x, prev_y = player.x - DIRECTION[player.d][0], player.y - DIRECTION[player.d][1]
                        self.player_move_map[player.x][player.y] = player.player_num
                        self.player_move_map[prev_x][prev_y] = 0
                        self.player_move_map[opposite.x][opposite.y] = opposite.player_num
                    else:
                        # player 짐 -> player가 움직여야 한다. 단, ignore하면 안 된다.
                        self.game_map[player.x][player.y].extend(player.guns[:])
                        player.guns = []

                        self.move(idx, ignore_player=False)
                        self.grab_gun(idx)

                        self.grab_gun(opposite_idx)

                        prev_x, prev_y = player.x - DIRECTION[player.d][0], player.y - DIRECTION[player.d][1]
                        self.player_move_map[player.x][player.y] = player.player_num
                        self.player_move_map[prev_x][prev_y] = 0
                        self.player_move_map[opposite.x][opposite.y] = opposite.player_num
                else:
                    prev_x, prev_y = player.x - DIRECTION[player.d][0], player.y - DIRECTION[player.d][1]
                    self.player_move_map[player.x][player.y] = player.player_num
                    self.player_move_map[prev_x][prev_y] = 0

                    self.grab_gun(idx)

    def display(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                print(self.player_move_map[i][j], end=" ")
            print()


n, m, k = list(map(int, input().split()))

input_map = [list(map(int, input().split())) for _ in range(n)]

players = []
for _ in range(m):
    players.append(list(map(int, input().split())))

game = Game(n, input_map, m)
game.initialize(players)
game.play(k)

for player in game.players:
    print(player.points, end=" ")