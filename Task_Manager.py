# Project: Task manager
# Run in terminal: pip install rich

# I swear I did this myself
# ngl, I somehow enjoyed the coding process and learnt A LOT of new things too ;)

# Rich documentation: https://rich.readthedocs.io/en/stable/introduction.html
# I definitely didn't spent like half of the time reading that

import os
import sys
from typing import (  #idk why I have to do this lol, but it looks "better" so ehhh
    #Literal,
    NoReturn,
    #Optional,
    Union,
)

if sys.stdout.encoding.lower().startswith('utf'):
    safe_mode = False # TODO: Add emojis, rich Progress Display feature
else:
    print("We detected that our console doesn't support UTF-8, program will start in safe mode.")
    safe_mode= True # TODO: Finish safe mode option
imi = False # IMI = Is module installed

def cin(text:str, kimsg:str = "\nError: KeyboardInterrupt. Program stopping.", stop: bool = True, rich: bool = False) -> Union[str, None, NoReturn]: #cin = custom input ; kimsg = KeyboardInterrupt message
    """Just like normal input(), but could handle KeyboardInterrupt

    Args:
        text (str): Similar to `prompt` parameter in input().
        kimsg (str, optional): What to print when KeyboardInterrupt happens. Defaults to "".
        stop (bool, optional): Instructs to stop the program. Defaults to True.
        rich (bool, optional): Use rich module or not. Defaults to False.
    """
    try:
        if rich and imi:
            from rich.console import Console
            console = Console()
            return console.input(text)
        elif (not rich) or (not imi):
            return input(text)
    except KeyboardInterrupt:
        print(kimsg)
        if stop:
            exit(None)
    except Exception as e:
        print(f"Unexpected error while running 'cin' function: {e}")
        exit(None)

# Does the check module thingy
if not safe_mode:
    try:
        from rich import box

        #from rich import print as rprint
        #from rich.columns import Columns
        from rich.console import Console

        #from rich.panel import Panel
        from rich.table import Table
        imi = True
        cin("Warning: You might need to resize your terminal (make it as tall as possible for the best experience)\nIf you're experiencing visual glitches, temporary uninstall rich and report to the Github issue page (press enter) ", rich=True)
        console = Console()
        console.rule("[bold purple]Task manager")
    except ModuleNotFoundError:
        try:
            if input('Please install "rich" module via pip (press enter to exit program)! Input "n" to continue, program will run normally without MOST of its features.\n> ') == "n":
                pass
            else:
                exit(None)
        except KeyboardInterrupt:
            exit(None)
    except ImportError:
        print("Please double check if you have 'rich' module installed. (ImportError)")
    except Exception as e:
        print(f"An unexpected error happened: {e}")


def options(options:list, title:str = None, prompt: str = "> ") -> Union[int, NoReturn]:
    """Display the options
    Args:
        title (str): Title.
        options (list): The options user could choose.
        prompt (str, optional): Just like `prompt` in input(). Defaults to "> ".
    """
    choices = []
    if imi:
        table = Table(title=title, box=box.MINIMAL)
        table.add_column("Press", justify="center", style="magenta")
        table.add_column("Content", justify="left", style="green")
        for n,option in enumerate(options):
            table.add_row(str(n+1), option)
            choices.append(str(n+1))
        console.print(table)
        v = cin(prompt)
    else:
        if title is not None:
            print(f"========={title}=========")
        for n, option in enumerate(options):
            print(f"{str(n+1)}. {option}")
            choices.append(str(n+1))
        v = cin(prompt)
    while (not v.isdigit()) or (v not in choices):
        print(f"Invalid choice. Choices: {choices}")
        v = cin(prompt)

    return int(v)

def display_tasks(tasks: dict, title:str = "Tasks") -> str:
    """Display the tasks
    Args:
        tasks (dict): Task list
        title (dict, optional): Title
    """
    commands = "Enter 'a' to add task(s)\nEnter 'r' to remove task(s)\nEnter 'e' to rename an existing task\nEnter 'o' to change the order of tasks\nEnter 'm' to mark task(s) as in progress or done\nEnter 'v1' to view only unfinished tasks\nEnter 'v2' to view only finished tasks\nEnter 'v' to show all tasks\nEnter 'b' to go back to menu"
    if imi:
        table = Table(title=title, box=box.DOUBLE, show_footer=True)
        if not tasks:
            table.add_column("Commands", "Note: This window showed up because task list is empty", justify="left", style="cyan")
            table.add_row(commands, style="bright_blue")
        else:
            table.add_column("No", "Commands", justify="center", style="cyan")
            table.add_column("Task", commands, justify="left", style="bright_white")
            table.add_column("Status", justify="center", style="blue_violet")
            for n, task in enumerate(tasks):
                if tasks[task] == "Unfinished":
                    table.add_row(str(n+1), str(task), str(tasks[task]), style="red")
                elif tasks[task] == "Finished":
                    table.add_row(str(n+1), str(task), str(tasks[task]), style="green")
                elif tasks[task] == "In progress":
                    table.add_row(str(n+1), str(task), str(tasks[task]), style="white")
                else:
                    table.add_row(str(n+1), str(task), str(tasks[task]))
        console.print(table)
    else:
        print("---Tasks---\nIndex | Task | Status")
        for n, task in enumerate(tasks):
            print(f"{str(n+1)}. {task} , {tasks[task]}")
        print("---Controls---")
        print(commands)
    return cin("> ")


# Asks for permission to write file
if not os.path.exists("task_manager_data.json"):
    if (a:=input("Do you allow this program to save a .json file to your computer?\n1. Yes\n2. No (program will still run)\n> ")) == "2":
        write = False
        cin("Warning: Data will be lost when the program stops (press enter) ")
    elif a == "1":
        write = True
    else:
        print("Invalid choice. Enter 1 or 2.")
else:
    write = True

#===========
class Data: # my first class EVER in python!! Feel free to leave feedback. # TODO: Add handling exceptions to class
    """(json) Data management class
    Args:
        file (str): Path to .json file (if path doesn't exist, a valid json file will be automatically created). If not provided, no json file will be written and data will be saved to memory.
    """

    def __init__(self, file:str = None):
        import json
        import os
        if not os.path.exists(file):
            with open(file, "w") as f:
                f.write("{\n\n}")
                f.flush() # For some reason it bugs out and this is a solution I found
                os.fsync(f.fileno())
            self.data = {}
        else:
            try:
                with open(file, "r") as f:
                    self.data = json.load(f)
            except json.decoder.JSONDecodeError:
                print("Invalid JSON data. Try deleting 'task_manager_data.json' in project directory. (json.decoder.JSONDecodeError)")
                exit(None)
            except Exception as e:
                print(f"Unexpected error in Data class: {e}")
        self.file = open(file, mode="r+", encoding="utf-8")
        self.path = file
    def __repr__(self):
        return f"Data('{self.file}')"
    def __str__(self):
        return f"Data: {self.data}\nData file: {self.path}"
    def __len__(self):
        return len(self.data)
    def __getitem__(self, key):
        return self.data[key]
    def __iter__(self):
        return iter(list(self.data.keys()))
    def add(self, data:dict) -> None:
        """Allows to add new keys or replace existing keys
        Args:
            data (dict): What to add. Multiple key-value pairs are supported. If key exist, the value will be replaced.
        """
        for key in data:
            self.data[key] = data[key]
    def delete(self, key: str | list[str]) -> None: # it took me literally HOURS to figure this out
        """Delete a key in data. Nested dictionary support.
        Args:
            key (Union[str,list]): The key to delete or key path (example: `delete(key=["a","b"])` will delete `data[a][b]`)
        """
        if isinstance(key, str):
            self.data.pop(key, None)
        elif isinstance(key, list) and key:
            current = self.data
            for k in key[:-1]:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return  # Key path doesn't exist, should've make an exception for this.. (I'm falling in love with classes)
            if isinstance(current, dict):
                current.pop(key[-1], None)
    def get(self) -> dict:
        """Returns the data. EXACTLY the same as `object.data`
        """
        return self.data
    def write(self) -> None:
        """Overwrite the json file with the new data
        """
        if self.path == "":
            return
        import json
        json.dump(self.data, open(self.path, mode="w", encoding="utf-8"), indent=4)
#===========

# I organized everything into functions for the convenience
if write:
    d = Data(file="task_manager_data.json")
    cin("Important: If you force stop the program (console shutdown, KeyboardInterrupt, etc), data will NOT be saved. (press enter) ")
else:
    d = Data()

def print_report():
    print("=========Report=========")
    finished = 0
    unfinished = 0
    total = 0
    for k in d.data:
        if d[k] == "Finished":
            finished += 1
        elif d[k] == "Unfinished":
            unfinished += 1
        total += 1
    try:
        print(f"You have completed {(finished / total) * 100}% of the tasks\nRatio of finished to unfinished is {finished}:{unfinished} (which is {(finished / unfinished) * 100}%)\n")
    except ZeroDivisionError:
        print(f"You have completed 0% of the tasks\nRatio of finished to unfinished is {finished}:{unfinished} (which is 0%)\n")
    cin("Press enter to go back to menu ")
    return "menu"

def tasks():
    print("=========Tasks=========")
    print("Tip: View tasks to see the commands\n")
    o = display_tasks(d.data)
    while True:
        key_list = list(d.data.keys())
        if o == "a": # Add
            aname = cin("Enter new task name: ")
            if aname.replace(" ", "") == "":
                print("Name cannot be empty")
            elif aname in d.data:
                print("Task names could not be the same")
            else:
                astatus = cin("Choose status for task:\n1. Unfinished\n2. In progress\n3. Finished\n> ")
                if astatus not in ["1", "2", "3"]:
                    print("Invalid status, Unfinished will be used.")
                    d.add({aname:"Unfinished"})
                else:
                    if astatus == "1":
                        d.add({aname:"Unfinished"})
                    elif astatus == "2":
                        d.add({aname:"In progress"})
                    elif astatus == "3":
                        d.add({aname:"Finished"})
                print(f"Task '{aname}' added successfully")
            o = cin("> ") # TODO: make custom input prompts for each "screen" (ex: "Tasks> ")

        elif o == "r": # Remove
            print("Tasks: Index | Name")
            for n, task in enumerate(d.data):
                print(f"{n+1}. {task}")
            ri = cin("Select the index(es) of task(s) to delete (example: 1,4,2): ") # i = Indexes
            ri = ri.replace(" ", "").split(",")

            delete_keys = []
            for ind in ri:
                if ind == "":
                    ri.remove("")
                    continue
                try:
                    ind = int(ind)
                except ValueError:
                    print("Invalid index list")
                    break
                if ind > len(d.data) or ind < 1:
                    print("Index doesn't exist")
                    break
                delete_keys.append(key_list[ind-1])
            if delete_keys: # If the list is not empty
                d.delete(delete_keys)
                print("Task deleted successfully")
            o = cin("> ")

        elif o == "e": # Edit
            print("Tasks: Index | Name")
            for n, task in enumerate(d.data):
                print(f"{n+1}. {task}")
            ei = cin("Select the task to rename: ")
            try:
                ei = int(ei)
                if 0 < ei <= len(d.data):
                    new_name = cin("Enter new task name: ")
                    if new_name.replace(" ", "") == "":
                        print("Name cannot be empty")
                    elif new_name in key_list:
                        print("Task name already exist")
                    else:
                        d.add({new_name:d.data[key_list[ei - 1]]}) # add key with the given name and old value
                        d.delete(key_list[ei - 1]) # delete the old key
                else:
                    print("Index doesn't exist")
            except ValueError:
                print("Invalid index")
            o = cin("> ")

        elif o == "o": # Change Order
            print("Tasks: Index | Name")
            for n, task in enumerate(d.data):
                print(f"{n+1}. {task}")
            oi = cin("Enter the reordered task list (example: 5,3,2,1,4): ") # i = Indexes
            oi = oi.replace(" ", "").split(",")
            old_data = d.data.copy()
            new_data = {}
            # Make a new dict with the order, then overwrite d.data
            for i in oi:
                try:
                    i = int(i)
                except ValueError:
                    print("Invalid index")
                    new_data = {}
                    break
                if i != "":
                    oname = key_list[i-1]
                    new_data[oname] = d.data[oname]
                    old_data.pop(oname, None)
            if old_data: # If old_data is not empty, add the remaining tasks
                for i in old_data:
                    new_data[i] = old_data[i]
            if new_data:
                d.data = new_data.copy()
            o = cin("> ")

        elif o == "m": # Mark as in progress/done
            print("Tasks: Index | Name")
            for n, task in enumerate(d.data):
                print(f"{n+1}. {task}")
            mi = cin("Enter task index to mark: ")
            try:
                mi = int(mi)
                if 0 < mi <= len(d.data):
                    mname = key_list[mi-1]
                    status = cin("Mark task as:\n1. Finished\n2. In progress\n3. Unfinished\n4. Custom status\n> ")
                    try:
                        status = int(status)
                        if status not in [1,2,3,4]:
                            print("Invalid choice")
                    except ValueError:
                        print("Invalid choice")
                    if status == 1:
                        d.add({str(mname):"Finished"})
                    elif status == 2:
                        d.add({str(mname):"In progress"})
                    elif status == 3:
                        d.add({str(mname):"Unfinished"})
                    elif status == 4:
                        cstatus = cin("Enter custom status: ")
                        if cstatus.replace(" ", "") == "":
                            print("Status cannot be empty")
                        d.add({str(mname):cstatus})
                    print("Task marked successfully")
                else:
                    print("Index doesn't exist")
            except ValueError:
                print("Invalid index")
            o = cin("> ")
        elif o == "v1": # Show unfinished tasks
            unfinished = {}
            for t in d.data:
                if d.data[t] == "Unfinished":
                    unfinished[t] = d.data[t]
            o = display_tasks(unfinished)
        elif o == "v2": # Show finished tasks
            finished = {}
            for t in d.data:
                if d.data[t] == "Finished":
                    finished[t] = d.data[t]
            o = display_tasks(finished)

        elif o == "v": # Show all tasks
            o = display_tasks(d)

        elif o == "b": # Back to menu
            return "menu"
        
        else:
            print("Invalid choice. Enter 'v' to show (tasks and) controls.")
            o = cin("> ")
def menu():
    if safe_mode:
        a = options(title="Menu", options=["View and modify tasks (add, remove, mark as done)", "Print report", "Disable safe mode", "Exit"])
        if a == 1:
            pass
    a = options(title="Menu", options=["View and modify tasks (add, remove, mark as done)", "Print report", "Reset", "Exit"])
    if a == 1:
        return "tasks"
    if a == 2:
        return "print_report"
    if a == 3:
        if input("Are you sure? All data will be lost. (y/n) ").lower() == "y":
            try:
                os.remove("task_manager_data.json")
            except FileNotFoundError:
                print("Data file (task_manager_data.json) doesn't exist")
                return "menu"
            except PermissionError:
                print("Cannot delete task_manager_data.json because of PermissionError (try deleting the file manually)")
                print("Attempting to overwrite file")
                try:
                    d.data = {}
                    d.write()
                    print("Data has been reset")
                except Exception as e:
                    print(f"Error: {e}")
                return "menu"
            except Exception as e:
                print(f"Unexpected error happened when program attempts to delete task_manager_data.json: {e}")
                return "menu"
            return "exit"
        return "menu"
    if a == 4:
        return "exit"



# The idea is to assign the functions to dictionary keys, then call them. And based on what the user chooses, the functions will return which function to call next.
func_map = {
    "menu": menu,
    "tasks": tasks,
    "print_report": print_report
}
run = "menu"
while run != "exit":
    run = func_map[run]
    run = run()
    """
    try:
        run = run()
    except Exception as e:
        print(f"Unexpected error while running program: {e}")
        if input("Enter 's' to save the data (look at the error, saving is not recommend if the error is related to file/data/json): ") == "s":
            break
        else:
            exit(None)
    """

d.write()