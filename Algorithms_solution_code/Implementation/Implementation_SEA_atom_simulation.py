DIRECTION = {
    0: [0, 1],
    1: [0, -1],
    2: [-1, 0],
    3: [1, 0]
}


class Atom:
    def __init__(self, x, y, direction, energy):
        self.x = x
        self.prev_x = x
        self.y = y
        self.prev_y = y

        self.direction = direction
        self.energy = energy


class PowerPlant:
    def __init__(self):
        self.atoms = []
        self.collision_energy = 0
        self.atom_locations = dict()

    def create_atom(self, x, y, direction, energy):
        self.atoms.append(Atom(x, y, direction, energy))

    def check_validity(self):
        to_be_collide_atom = set()
        for i in range(len(self.atoms)):
            for j in range(len(self.atoms)):
                if i == j: continue
                to_be_insert = False

                if self.atoms[i].direction == 0:
                    if self.atoms[j].direction == 1 and self.atoms[i].x == self.atoms[j].x:
                        to_be_insert = True
                    elif self.atoms[j].direction == 2:
                        if self.atoms[j].x - self.atoms[i].x == self.atoms[j].y - self.atoms[i].y:
                            to_be_insert = True
                    elif self.atoms[j].direction == 3:
                        if self.atoms[i].x - self.atoms[j].x == self.atoms[j].y - self.atoms[i].y:
                            to_be_insert = True

                elif self.atoms[i].direction == 1:
                    if self.atoms[j].direction == 0 and self.atoms[i].x == self.atoms[j].x:
                        to_be_insert = True
                    elif self.atoms[j].direction == 2:
                        if self.atoms[j].x - self.atoms[i].x == self.atoms[i].y - self.atoms[j].y:
                            to_be_insert = True
                    elif self.atoms[j].direction == 3:
                        if self.atoms[i].x - self.atoms[j].x == self.atoms[i].y - self.atoms[j].y:
                            to_be_insert = True

                elif self.atoms[i].direction == 2:
                    if self.atoms[j].direction == 3 and self.atoms[i].y == self.atoms[j].y:
                        to_be_insert = True
                    elif self.atoms[j].direction == 0:
                        if self.atoms[i].x - self.atoms[j].x == self.atoms[i].y - self.atoms[j].y:
                            to_be_insert = True
                    elif self.atoms[j].direction == 1:
                        if self.atoms[i].x - self.atoms[j].x == self.atoms[j].y - self.atoms[i].y:
                            to_be_insert = True

                elif self.atoms[i].direction == 3:
                    if self.atoms[j].direction == 2 and self.atoms[i].y == self.atoms[j].y:
                        to_be_insert = True
                    elif self.atoms[j].direction == 0:
                        if self.atoms[j].x - self.atoms[i].x == self.atoms[i].y - self.atoms[j].y:
                            to_be_insert = True
                    elif self.atoms[j].direction == 1:
                        if self.atoms[j].x - self.atoms[i].x == self.atoms[j].y - self.atoms[i].y:
                            to_be_insert = True

                if to_be_insert:
                    to_be_collide_atom.add(i)
                    to_be_collide_atom.add(j)

        temp_atoms = []
        for idx in to_be_collide_atom:
            temp_atoms.append(self.atoms[idx])

        self.atoms = temp_atoms

    def move_atoms(self):
        velocity = 0.5

        self.atom_locations = dict()

        is_there_collision = False
        for idx, atom in enumerate(self.atoms):
            dx, dy = DIRECTION[atom.direction]

            self.atoms[idx].prev_x = self.atoms[idx].x
            self.atoms[idx].prev_y = self.atoms[idx].y

            self.atoms[idx].x = self.atoms[idx].x + dx * velocity
            self.atoms[idx].y = self.atoms[idx].y + dy * velocity

            keys = [
                f"{self.atoms[idx].x}_{self.atoms[idx].y}"
                ]
            for key in keys:
                value = self.atom_locations.get(key, None)
                if value is None:
                    self.atom_locations[key] = [idx]
                else:
                    self.atom_locations[key].append(idx)
                    is_there_collision = True

        return is_there_collision

    def check_collision(self):
        keys = self.atom_locations.keys()
        to_be_removed_atoms = set()
        for key in keys:
            if len(self.atom_locations[key]) > 1:
                for idx in self.atom_locations[key]:
                    to_be_removed_atoms.add(idx)

        temp_atoms = []
        for idx in range(len(self.atoms)):
            if idx not in to_be_removed_atoms:
                temp_atoms.append(self.atoms[idx])
            else:
                self.collision_energy = self.collision_energy + self.atoms[idx].energy
        self.atoms = temp_atoms


T = int(input())
for t_iter in range(1, T + 1):
    N = int(input())

    power_plant = PowerPlant()
    for n_iter in range(N):
        x, y, direction, energy = list(map(int, input().split()))
        power_plant.create_atom(x, y, direction, energy)

    power_plant.check_validity()

    for _ in range(4000):
        is_there_collision = power_plant.move_atoms()
        if is_there_collision: power_plant.check_collision()

    print(f"#{t_iter} {power_plant.collision_energy}")