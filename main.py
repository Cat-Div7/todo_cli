import argparse

parser = argparse.ArgumentParser(description='Todo CLI')

parser.add_argument('command')
parser.add_argument('task', nargs='?')

args = parser.parse_args()

print(args.command)
print(args.task)