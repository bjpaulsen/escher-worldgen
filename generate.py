from constraint import *
import random
import escher
import sys

# system defaults
world_width = 6
world_length = 6
world_height = 6

world = [(x, y, z) for x in range(world_width) for y in range(world_length) for z in range(world_height)]

problem = Problem(RecursiveBacktrackingSolver())

'''
GENERATE.PY

This program generates a 3D Escher-like World that can be imported into a Unity scene.
Using the command line interface, you can specify the dimensions, block density, stair behavior,
and other placement rules. Other constraints are static to ensure certain world qualities.

Each world generated will be different, starting with a semi-random base. Constraints on top
of that base create the rest of the world.

'''

command_line_interface = '''
        usage:
        \t\t\t[pythonversion] generate.py [width] [length] [height] [density] (optional constraints...)
        
        optional constraints:
        \t\t\tlayerHasStairs  \t - require each layer to have at least 1 stair (recommended)
        \t\t\tlayerHasAir     \t - require each layer to have a percentage of air (may be slow)
        \t\t\tblockHasNeighbor\t - prevent floating blocks, encourage navigable paths (may be slow)
        
        note: all arguments are optional, but must be in order
        '''

# The following constraints are for testing / experimenting purposes

# blockHasNeighbor ensures that each block has at least one neighboring non-air space.
# inputs: 
#   - the current location being looked at. If it's a block, this constraint applies
#   - a list of directly adjacent spaces. if any of these are blocks, the constraint passes
def blockHasNeighbor(location, *adj):
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
    return num_a >= len(layer)/2


# guarantee that each vertical layer has at least 1 stair
def layerHasStairs(*layer):
    return 's' in layer


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


# main method to generate a level
def generate():

    # setup the 3D grid of locations to be filled in
    for x in range(world_width):
        for y in range(world_length):
            for z in range(world_height):
                problem.addVariable((x, y, z), escher.blocks)

    # ~23% of volume should be blocks unless otherwise specified
    density = .23148

    # input density as 4th argument (float between 0 and 1)
    if len(sys.argv) >= 5:
        density = float(sys.argv[4])
        
    # create random start to the level
    starter_blocks = round(density * world_width * world_length * world_height)
    for j in range(starter_blocks):
        problem.addConstraint(InSetConstraint(['b']), [(random.randint(0, world_width-1), random.randint(0, world_length-1), random.randint(0, world_height-1))])
        
    # add positional constraints to stairs, blocks, air
    for z in range(world_height):
        
        # require each layer to have a percentage of air if specified
        if 'layerHasAir' in sys.argv:
            problem.addConstraint(layerHasAir, [(a, b, z) for a in range(world_width) for b in range(world_length)])
        
        # require each layer to have stairs if specified
        if 'layerHasStairs' in sys.argv:
            problem.addConstraint(layerHasStairs, [(a, b, z) for a in range(world_width) for b in range(world_length)])
        
        for y in range(world_length):
            for x in range(world_width):
                adj = [(a, b, c) for a in range(x-1, x+2) for b in range(y-1, y+2) for c in range(z-1, z+2) if inRange(x, y, z, a, b, c)]
                blockNeighbors = [(x, y, z)]
                blockNeighbors.extend(adj)
                
                # prevent floating blocks if specified
                if 'blockHasNeighbor' in sys.argv:
                    problem.addConstraint(blockHasNeighbor, blockNeighbors)
                
                # always use stairsWalkable, essential constraint
                problem.addConstraint(stairsWalkable, blockNeighbors)
    
    # create a level that satisfies the constraints, if possible
    solution = problem.getSolution()

    # print the level in a format we can import into Unity
    world = []
    for z in range(world_height):
        for y in range(world_length):
            for x in range(world_width):
                print(solution[(x, y, z)], end='')
            print()
        if z+1 < world_height:
            print('X')


# start of program, command line interface
if __name__ == '__main__':
    if len(sys.argv) == 2 and (sys.argv[1] == 'help' or sys.argv[1] == '--help'):
        print(command_line_interface)
    else:
        # command line inputs determine level size
        if len(sys.argv) >= 2 and sys.argv[1].isdigit():
            world_width = int(sys.argv[1])
            if len(sys.argv) >= 3 and sys.argv[2].isdigit():
                world_length = int(sys.argv[2])
                if len(sys.argv) >= 4 and sys.argv[3].isdigit():
                    world_height = int(sys.argv[3])
        generate()
