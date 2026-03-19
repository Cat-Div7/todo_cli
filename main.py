import argparse
import json 

parser = argparse.ArgumentParser(description='Todo CLI')
subparsers = parser.add_subparsers(dest='command')

add_parser = subparsers.add_parser('add', help='Add a new task')

add_parser.add_argument('task', type=str, help='The task description')
list_parser = subparsers.add_parser('list', help='List all tasks')

args = parser.parse_args()
command = args.command

def add_task(task):
  # Read existing tasks
  try:
    with open('tasks.json', 'r') as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Append new task
  curr_tasks.append({"title": task, "done": False})
  # Write the updated tasks back to the file
  with open('tasks.json', 'w') as f:
    json.dump(curr_tasks, f, indent=2)

def list_tasks():
  # Open Folder and read tasks
  try:
    with open('tasks.json', 'r') as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Return if no tasks
  if not curr_tasks:
    print('No tasks yet!')
    return

  # Display tasks
  print("Your Tasks:")
  for idx, task in enumerate(curr_tasks, start=1):
    status = 'Done' if task['done'] else 'Not Done'
    print(f"[{idx}] {task['title']} - {status}")

if not args.command:
    parser.print_help()

if command == 'add':
  add_task(args.task)
  print('Task Added')

elif command == 'list':
  list_tasks()
