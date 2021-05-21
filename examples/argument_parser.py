import argparse


parser = argparse.ArgumentParser('apply or revert migration')
parser.add_argument('name', help='shit')
parser.add_argument('-down', '-d', action='store_const', const='down', default='up',
                    help='if this setted revert migrations')
parser.add_argument('-count', type=int, default=0)
parser.add_argument('-auto-confirm', '-c', action='store_true', default=False)

if __name__ == '__main__':
    arguments = parser.parse_args()
    print((arguments.name, arguments.down, arguments.count, arguments.auto_confirm))
