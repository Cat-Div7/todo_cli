import argparse
import json 

FILE_NAME = 'tasks.json'

parser = argparse.ArgumentParser(description='Todo CLI')
subparsers = parser.add_subparsers(dest='command')

add_parser = subparsers.add_parser('add', help='Add a new task')
list_parser = subparsers.add_parser('list', help='List all tasks')
done_parser = subparsers.add_parser('done', help='Mark task as done')
delete_parser = subparsers.add_parser('delete', help='Delete a task')
update_parser = subparsers.add_parser('update', help='Update a task')

add_parser.add_argument('task', type=str, help='The task description')
add_parser.add_argument('-p', '--priority', type=str, choices=['high', 'medium', 'low'], default='medium' ,help='Task priority (high, medium, low)')
list_parser.add_argument('-p', '--priority', type=str, choices=['high', 'medium', 'low'],help='Filter tasks by priority')
done_parser.add_argument('index', type=int, help='Task number to mark as done')
delete_parser.add_argument('index', type=int, help='Task number to delete')
update_parser.add_argument('index', type=int, help='Task number to update')
update_parser.add_argument('new_title', type=str, help='New task title')

args = parser.parse_args()
command = args.command

def load_tasks():
  try:
    with open(FILE_NAME, 'r') as f:
      return json.load(f)
  except (json.JSONDecodeError, FileNotFoundError):
    return []

def save_tasks(tasks):
  with open(FILE_NAME, 'w') as f:
    json.dump(tasks, f, indent=2)

def add_task(task, priority):
  # Read existing tasks
  curr_tasks = load_tasks()
  # Append new task
  curr_tasks.append({"title": task, "done": False, "priority": priority})
  # Write the updated tasks
  save_tasks(curr_tasks)

def list_tasks(filter_priority=None):
  # Read existing tasks
  curr_tasks = load_tasks()

  # Filter priority
  if filter_priority:
    curr_tasks = [
      task for task in curr_tasks
      if task['priority'] == filter_priority
    ]
    if not curr_tasks:
      print('No tasks match this priority')
      return

  # Return if no tasks
  if not curr_tasks:
    print('No tasks yet!')
    return

  # Display tasks
  print("Your Tasks:")
  for idx, task in enumerate(curr_tasks, start=1):
    status = 'Done' if task['done'] else 'Not Done'
    priority = task['priority'].upper()
    print(f"[{idx}] ({priority}) {task['title']} - {status}")

def mark_done(task_number):
  # Read existing tasks
  curr_tasks = load_tasks()

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

      # Write the updated tasks
      save_tasks(curr_tasks)

      print(f'Task {task_number} marked as done.')
    else:
      print('Operation cancelled.')
  else:
    print('Invalid task number.')

def delete_task(task_number):
  # Read existing tasks
  curr_tasks = load_tasks()

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

      # Write the updated tasks
      save_tasks(curr_tasks)

      print(f'Task {task_number} deleted succesfully.')
    else:
      print('Operation cancelled.')
  else:
    print('Invalid task number.')

def update_task(task_number, new_title):
  # Read existing tasks
  curr_tasks = load_tasks()

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

      # Write the updated tasks
      save_tasks(curr_tasks)

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
  list_tasks(args.priority)

elif command == 'done':
  mark_done(args.index)

elif command == 'delete':
  delete_task(args.index)

elif command == 'update':
  update_task(args.index, args.new_title)