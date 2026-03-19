import argparse
import json 

parser = argparse.ArgumentParser(description='Todo CLI')

parser.add_argument('command')
parser.add_argument('task', nargs='?')

args = parser.parse_args()

command = args.command
task = args.task

def add_task(task):
  # Read existing tasks
  try:
    with open('tasks.json', 'r') as f:
      curr_tasks = json.load(f)
  except json.JSONDecodeError:
    curr_tasks = []
  except FileNotFoundError:
    curr_tasks = []

  # Append new task
  curr_tasks.append({"Title": task, "done": False})
  # Write the updated tasks back to the file
  with open('tasks.json', 'w') as f:
    json.dump(curr_tasks, f, indent=2)

if command == 'add':
  add_task(task)
  print('Task Added')