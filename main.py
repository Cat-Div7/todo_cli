import argparse
import json 

parser = argparse.ArgumentParser(description='Todo CLI')
subparsers = parser.add_subparsers(dest='command')

add_parser = subparsers.add_parser('add', help='Add a new task')
list_parser = subparsers.add_parser('list', help='List all tasks')
done_parser = subparsers.add_parser('done', help='Mark task as done')
delete_parser = subparsers.add_parser('delete', help='Delete a task')
update_parser = subparsers.add_parser('update', help='Update a task')

add_parser.add_argument('task', type=str, help='The task description')
add_parser.add_argument('-p', '--priority', type=str, choices=['high', 'medium', 'low'], default='medium' ,help='Task priority (high, medium, low)')
done_parser.add_argument('index', type=int, help='Task number to mark as done')
delete_parser.add_argument('index', type=int, help='Task number to delete')
update_parser.add_argument('index', type=int, help='Task number to update')
update_parser.add_argument('new_title', type=str, help='New task title')

args = parser.parse_args()
command = args.command

def add_task(task, priority):
  # Read existing tasks
  try:
    with open('tasks.json', 'r') as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Append new task
  curr_tasks.append({"title": task, "done": False, "priority": priority})
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

def mark_done(task_number):
  # Open Folder and read tasks
  try: 
    with open('tasks.json', 'r')as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Return if no tasks
  if not curr_tasks:
    print('No tasks available')
    return

  # Validate task number
  if 0 < task_number <= len(curr_tasks):
    task = curr_tasks[task_number - 1]
    
    # Check if task is already done
    if task['done']:
      print(f"Task {task_number} is already done ✔")
      return

    print('The task you want to mark as done is:')
    print(f"{task['title']}")

    # Confirmation before marking as done
    confirm = input("Confirm? (Y/n): ").lower()

    if confirm == "y":
      task['done'] = True

      with open('tasks.json', 'w') as f:
        json.dump(curr_tasks, f, indent=2)

      print(f'Task {task_number} marked as done.')
    else:
      print('Operation cancelled.')
  else:
    print('Invalid task number.')

def delete_task(task_number):
  # Open Folder and read tasks
  try: 
    with open('tasks.json', 'r')as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Return if no tasks
  if not curr_tasks:
    print('No tasks available')
    return

  # Validate task number
  if 0 < task_number <= len(curr_tasks):
    task = curr_tasks[task_number - 1]

    print('The task you want to delete is:')
    print(f"{task['title']}")

    # Confirmation before deleting
    confirm = input("Confirm Deleting? (Y/n): ").lower()

    if confirm == "y":
      curr_tasks.pop(task_number - 1)

      with open('tasks.json', 'w') as f:
        json.dump(curr_tasks, f, indent=2)

      print(f'Task {task_number} deleted succesfully.')
    else:
      print('Operation cancelled.')
  else:
    print('Invalid task number.')

def update_task(task_number, new_title):
  # Open Folder and read tasks
  try: 
    with open('tasks.json', 'r')as f:
      curr_tasks = json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    curr_tasks = []

  # Return if no tasks
  if not curr_tasks:
    print('No tasks available')
    return

  # Validate task number
  if 0 < task_number <= len(curr_tasks):
    task = curr_tasks[task_number - 1]

    print(f"Current task: {task['title']}")
    print(f"New title: {new_title}")
    # Confirmation before updating
    confirm = input("Confirm update? (Y/n): ").lower()

    if confirm == "y":
      task['title'] = new_title

      with open('tasks.json', 'w') as f:
        json.dump(curr_tasks, f, indent=2)

      print(f'Task {task_number} updated succesfully.')
    else:
      print('Operation cancelled.')
  else:
    print('Invalid task number.')

if not args.command:
    parser.print_help()

elif command == 'add':
  add_task(args.task, args.priority)
  print('Task Added')

elif command == 'list':
  list_tasks()

elif command == 'done':
  mark_done(args.index)

elif command == 'delete':
  delete_task(args.index)

elif command == 'update':
  update_task(args.index, args.new_title)