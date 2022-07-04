import sys
from spaceship.game import SpaceShip


def main(args):
    return SpaceShip(args).start()

if __name__ == '__main__':
    sys.exit(main(sys.argv))