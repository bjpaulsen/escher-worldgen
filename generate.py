from constraint import *
import escher

world_width = 3
world_length = 3
world_height = 3

world = [(x, y, z) for x in range(world_width) for y in range(world_length) for z in range(world_height)]

problem = Problem()



def blockHasNeighbor(location, *adj):
    print()
    print(location)
    print(adj)
    if location == 'b':
        for neighbor in adj:
            if neighbor != '-':
                return True
    return False

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

    for x in range(world_width):
        for y in range(world_length):
            for z in range(world_height):
                adj = [(a, b, c) for a in range(x-1, x+2) for b in range(y-1, y+2) for c in range(z-1, z+2) if inRange(x, y, z, a, b, c)]
                
                # problem.addConstraint(SomeInSetConstraint(['-']), adj)
                # problem.addConstraint(SomeInSetConstraint(['b']), adj)
                # problem.addConstraint(FunctionConstraint(blockHasNeighbor, [(x, y, z)].extend(adj)))
                # problem.addConstraint(InSetConstraint(['b']), [(1, 1, 1)])
    

    # problem.addConstraint(SomeInSetConstraint(['s']))
    # problem.addConstraint(SomeInSetConstraint(['b']))
    
    solution = problem.getSolution()

    world = []
    for x in range(world_width):
        for y in range(world_length):
            for z in range(world_height):
                # world[x][y][z] = solution[(x, y, z)]
                print(solution[(x, y, z)], end='')
            print()
        print()

if __name__ == '__main__':
    generate()