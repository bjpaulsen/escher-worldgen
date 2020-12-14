from constraint import *
import escher

world_width = 3
world_length = 3
world_height = 3

world = [(x, y, z) for x in range(world_width) for y in range(world_length) for z in range(world_height)]

problem = Problem(RecursiveBacktrackingSolver())


'''
definitions:
    neighbor - each block has 6 neighbors (unless it's against a wall)

CONSTRAINT IDEAS (Test and see what works well)
    1. Solid blocks must have a neighbor (can't be free floating)
    2. Stairs must have at least 2 neighbors (places to walk to and from)
    3. Stairs must have at least 2 adjacent neighboring air blocks (space to walk in)
    4. Some minimum amount of air, blocks, stairs, etc

    * Stairs cannot be directly adjacent (cardinal) to other stairs?

OTHER THINGS TO IMPLEMENT
    1. Instead of representing types of blocks as characters, represent them as classes with 
    some basic information about the block.
        - Stairs have info about which sides are walkable
        - solid blocks or bridges etc. might have info about which decorations they have
'''

# The following constraints are for testing / experimenting purposes

# blockHasNeighbor ensures that each block has at least one neighboring non-air space.
# inputs: 
#   - the current location being looked at. If it's a block, this constraint applies
#   - a list of directly adjacent spaces. if any of these are non-air, the constraint passes
def blockHasNeighbor(location, *adj):
    # print()
    # print("location: ", location)
    # print("adj: ", adj)
    if location == 'b' or location == 's':
        for neighbor in adj:
            if neighbor != '-':
                return True
        return False
    return True


# guarantee that we can make stairs walkable by having enough neighboring blocks and air
def stairsWalkable(location, *adj):
    if location == 's':
        num_b = 0
        num_a = 0
        num_walls = 6-len(adj)
        for neighbor in adj:
            if neighbor == 'b':
                num_b += 1
            elif neighbor == '-':
                num_a += 1
        return num_b+num_walls >= 2 and num_a >= 2
    return True

# each layer has a percentage of air
def layerHasAir(*layer):
    print(layer)
    num_a = 0
    for block in layer:
        if block == '-':
            num_a += 1
    return num_a >= 2*len(layer)/3

# This constraint works! It ensures that the entire level is filled with stairs
def onlyStairs(location):
    if location == 's':
        return True
    return False

# checks if an adjacent position is in the world
# x y z is a legal position
# a b c is an adjacent position to be checked
def inRange(x, y, z, a, b, c):
    # checks that they are not the same position (collision)
    if a == x and b == y and c == z:
        return False
    # checks that at least 2 coordinates are the same (adjacency)
    if not ((a == x and b == y) or (b == y and c == z) or (a == x and c == z)):
        return False
    # checks that they are in the world (legality)
    if a < 0 or b < 0 or c < 0:
        return False
    if a >= world_width or b >= world_length or c >= world_height:
        return False
    return True

def generate():

    # setup the 3D grid of locations to be filled in
    for x in range(world_width):
        for y in range(world_length):
            for z in range(world_height):
                problem.addVariable((x, y, z), escher.blocks)

    for z in range(world_height):
        problem.addConstraint(layerHasAir, [(a, b, z) for a in range(world_width) for b in range(world_length)])
        for y in range(world_length):
            for x in range(world_width):
                adj = [(a, b, c) for a in range(x-1, x+2) for b in range(y-1, y+2) for c in range(z-1, z+2) if inRange(x, y, z, a, b, c)]
                blockNeighbors = [(x, y, z)]
                blockNeighbors.extend(adj)
                # print("blockNeighbors: ", blockNeighbors)
                # problem.addConstraint(blockHasNeighbor, blockNeighbors)
                problem.addConstraint(stairsWalkable, blockNeighbors)
    

    problem.addConstraint(SomeInSetConstraint(['s'], 4))
    # problem.addConstraint(SomeInSetConstraint(['b'], 5))
    # problem.addConstraint(SomeInSetConstraint(['-'], 35))
    # problem.addConstraint(SomeInSetConstraint(['b'], 5))

    print("done setting up, getting solution")
    print()
    
    solution = problem.getSolution()

    world = []
    for z in range(world_height):
        for y in range(world_length):
            for x in range(world_width):
                # world[x][y][z] = solution[(x, y, z)]
                print(solution[(x, y, z)], end='')
            print()
        print()

if __name__ == '__main__':
    generate()
