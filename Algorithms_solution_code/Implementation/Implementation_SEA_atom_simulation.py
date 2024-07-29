DIRECTION = {
    0: [0, 1],
    1: [0, -1],
    2: [-1, 0],
    3: [1, 0]
}
 
 
class Atom:
    def __init__(self, x, y, direction, energy):
        self.x = x
        self.y = y
        self.direction = direction
        self.energy = energy
 
 
class PowerPlant:
    def __init__(self):
        self.atoms = []
        self.collision_energy = 0
 
    def create_atom(self, x, y, direction, energy):
        self.atoms.append(Atom(x, y, direction, energy))
     
    def move_atoms(self):
        # Move atoms every 0.5 second
        for idx, atom in enumerate(self.atoms):
            dx, dy = DIRECTION[atom.direction]
 
            self.atoms[idx].x = self.atoms[idx].x + dx * 0.5
            self.atoms[idx].y = self.atoms[idx].y + dy * 0.5
 
    def check_collision(self):
        to_be_removed_atoms = set()
 
        validity = False
        for i in range(len(self.atoms)):
            if i in to_be_removed_atoms: continue
            for j in range(len(self.atoms)):
                if i == j: continue
                if j in to_be_removed_atoms: continue
                if self.atoms[i].x == self.atoms[j].x and self.atoms[i].y == self.atoms[j].y:
                    to_be_removed_atoms.add(j)
                    to_be_removed_atoms.add(i)
                else:
                    if not validity:
                        validity = self.check_validity_with_arguments(i, j)
         
        temp_atoms = []
        for i in range(len(self.atoms)):
            if i not in to_be_removed_atoms:
                temp_atoms.append(self.atoms[i])
            else:
                self.collision_energy = self.collision_energy + self.atoms[i].energy
        self.atoms = temp_atoms

        return validity
    
    def check_validity_with_arguments(self, atom_idx, d_atom_idx):
        if self.atoms[atom_idx].direction == 0:
            if self.atoms[d_atom_idx].direction == 1:
                if self.atoms[atom_idx].x == self.atoms[d_atom_idx].x:
                    return True
            elif self.atoms[d_atom_idx].direction == 2:
                if self.atoms[d_atom_idx].y > self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[d_atom_idx].y - self.atoms[atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 3:
                if self.atoms[d_atom_idx].y > self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[atom_idx].y - self.atoms[d_atom_idx].y:
                        return True
            
        elif self.atoms[atom_idx].direction == 1:
            if self.atoms[d_atom_idx].direction == 0:
                if self.atoms[atom_idx].x == self.atoms[d_atom_idx].x:
                    return True
            elif self.atoms[d_atom_idx].direction == 2:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[atom_idx].y - self.atoms[d_atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 3:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[d_atom_idx].y - self.atoms[atom_idx].y:
                        return True
            
        elif self.atoms[atom_idx].direction == 2:
            if self.atoms[d_atom_idx].direction == 0:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[atom_idx].y - self.atoms[d_atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 1:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[d_atom_idx].y - self.atoms[atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 3:
                if self.atoms[d_atom_idx].x == self.atoms[atom_idx].x:
                    return True
            
        elif self.atoms[atom_idx].direction == 3:
            if self.atoms[d_atom_idx].direction == 0:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[d_atom_idx].y - self.atoms[atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 1:
                if self.atoms[d_atom_idx].y < self.atoms[atom_idx].y:
                    if self.atoms[d_atom_idx].x - self.atoms[atom_idx].x == self.atoms[atom_idx].y - self.atoms[d_atom_idx].y:
                        return True
            elif self.atoms[d_atom_idx].direction == 3:
                if self.atoms[d_atom_idx].x == self.atoms[atom_idx].x:
                    return True
        return False
 
 
T = int(input())
for t_iter in range(1, T+1):
    N = int(input())
 
    power_plant = PowerPlant()
    for n_iter in range(N):
        x, y, direction, energy = list(map(int, input().split()))
        power_plant.create_atom(x, y, direction, energy)
 
    is_valid = True
    while is_valid:
        power_plant.move_atoms()
        is_valid = power_plant.check_collision()
     
    print(f"#{t_iter} {power_plant.collision_energy}")