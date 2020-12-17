from constraint import *
import random
import escher

world_width = 6
world_length = 6
world_height = 6

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
    if location == 'b':
        return 'b' in adj
    return True


# guarantee that we can make stairs walkable by having enough neighboring blocks and air
def stairsWalkable(location, *adj):
    if location == 's':
        num_b = 0
        for neighbor in adj:
            if neighbor == 'b':
                num_b += 1
        return num_b >= 2
    return True

# each layer has a percentage of air
def layerHasAir(*layer):
    num_a = 0
    for block in layer:
        if block == '-':
            num_a += 1
    return num_a >= 4*len(layer)/7

def layerHasStairs(*layer):
    num_s = 0
    for block in layer:
        if block == 's':
            num_s += 1
        if num_s >= 1:
            return True
    return False

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

    # create random start to the level
    for j in range(50):
        problem.addConstraint(InSetConstraint(['b']), [(random.randint(0, world_width-1), random.randint(0, world_length-1), random.randint(0, world_height-1))])
        
    for z in range(world_height):
        # problem.addConstraint(layerHasAir, [(a, b, z) for a in range(world_width) for b in range(world_length)])
        problem.addConstraint(layerHasStairs, [(a, b, z) for a in range(world_width) for b in range(world_length)])
        for y in range(world_length):
            for x in range(world_width):
                adj = [(a, b, c) for a in range(x-1, x+2) for b in range(y-1, y+2) for c in range(z-1, z+2) if inRange(x, y, z, a, b, c)]
                blockNeighbors = [(x, y, z)]
                blockNeighbors.extend(adj)
                # print("blockNeighbors: ", blockNeighbors)
                # problem.addConstraint(blockHasNeighbor, blockNeighbors)
                problem.addConstraint(stairsWalkable, blockNeighbors)
    

    problem.addConstraint(SomeInSetConstraint(['s'], 10))
    # problem.addConstraint(SomeInSetConstraint(['b'], 36))
    # problem.addConstraint(SomeInSetConstraint(['-'], 1))
    
    solution = problem.getSolution()

    world = []
    for z in range(world_height):
        for y in range(world_length):
            for x in range(world_width):
                # world[x][y][z] = solution[(x, y, z)]
                print(solution[(x, y, z)], end='')
            print()
        if z+1 < world_height:
            print('X')

if __name__ == '__main__':
    generate()
