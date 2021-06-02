import argparse


parser = argparse.ArgumentParser('example for argparse')
parser.add_argument('name', help='shit', default='default name')
parser.add_argument('-down', '-d', action='store_const', const='down', default='up',
                    help='if this setted revert migrations')
parser.add_argument('-count', type=int, default=0)
parser.add_argument('-auto-confirm', '-c', action='store_true', dest='dest', default=False)

if __name__ == '__main__':
    arguments = parser.parse_args()
    print(('name ', arguments.name, ', flag 1 ', arguments.down, ', flag 2 ', arguments.count, ', auto confitm ', arguments.dest))
