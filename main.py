import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import json


# ==================== Data Structure Classes ====================
class QueueToDo:
    def __init__(self):
        self.tasks = deque()

    def add_task(self, task):
        self.tasks.append(task)

    def complete_task(self):
        return self.tasks.popleft() if self.tasks else None

    def get_all_tasks(self):
        return list(self.tasks)

    def clear(self):
        self.tasks.clear()


class StackToDo:
    def __init__(self):
        self.tasks = []
        self.completed_stack = []

    def add_task(self, task):
        self.tasks.append(task)

    def complete_task(self):
        if self.tasks:
            completed = self.tasks.pop()
            self.completed_stack.append(completed)
            return completed
        return None

    def get_all_tasks(self):
        return self.tasks.copy()

    def get_history(self):
        return self.completed_stack.copy()

    def clear(self):
        self.tasks.clear()


class LinkedListToDo:
    class Node:
        def __init__(self, task):
            self.task = task
            self.next = None

    def __init__(self):
        self.head = None
        self.size = 0

    def add_task(self, task, position=None):
        new_node = self.Node(task)
        if position is None or position >= self.size:
            position = self.size
        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.size += 1

    def complete_task(self, position=0):
        if position < 0 or position >= self.size:
            return None
        if position == 0:
            completed = self.head.task
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            completed = current.next.task
            current.next = current.next.next
        self.size -= 1
        return completed

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task)
            current = current.next
        return tasks

    def clear(self):
        self.head = None
        self.size = 0


class BSTToDo:
    class Node:
        def __init__(self, priority, task):
            self.priority = priority
            self.task = task
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def add_task(self, priority, task):
        self.root = self._insert(self.root, priority, task)

    def _insert(self, node, priority, task):
        if node is None:
            return self.Node(priority, task)
        if priority < node.priority:
            node.left = self._insert(node.left, priority, task)
        else:
            node.right = self._insert(node.right, priority, task)
        return node

    def complete_highest_priority(self):
        if not self.root:
            return None
        parent, current = None, self.root
        while current.right:
            parent, current = current, current.right
        if parent:
            parent.right = current.left
        else:
            self.root = current.left
        return current.task

    def get_all_tasks(self):
        tasks = []
        self._inorder(self.root, tasks)
        return tasks

    def _inorder(self, node, tasks):
        if node:
            self._inorder(node.right, tasks)
            tasks.append(f"P{node.priority}: {node.task}")
            self._inorder(node.left, tasks)

    def clear(self):
        self.root = None


# ==================== Main Application ====================
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Structures To-Do App")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f5")

        # Color palette
        self.colors = {
            "primary": "#4a6fa5",
            "secondary": "#166088",
            "accent": "#4fc3f7",
            "danger": "#ff5252",
            "success": "#4caf50",
            "warning": "#ff9800",
            "dark": "#212121",
            "light": "#f5f5f5"
        }

        # Data structures
        self.queue = QueueToDo()
        self.stack = StackToDo()
        self.linked_list = LinkedListToDo()
        self.bst = BSTToDo()
        self.current_ds = "Queue"
        self.ds_map = {
            "Queue": self.queue,
            "Stack": self.stack,
            "Linked List": self.linked_list,
            "BST": self.bst
        }

        # Priority variable for BST
        self.priority_var = tk.IntVar(value=1)

        # Setup UI
        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.colors["primary"])
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        tk.Label(
            header_frame,
            text="Data Structures To-Do App",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors["primary"],
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        # Mode selection
        mode_frame = tk.Frame(header_frame, bg=self.colors["primary"])
        mode_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(
            mode_frame,
            text="Mode:",
            font=("Segoe UI", 10),
            bg=self.colors["primary"],
            fg="white"
        ).pack(side=tk.LEFT)

        self.mode_var = tk.StringVar(value="Queue")
        modes = ["Queue", "Stack", "Linked List", "BST"]
        mode_menu = ttk.OptionMenu(
            mode_frame, self.mode_var, "Queue", *modes, command=self.change_mode
        )
        mode_menu.config(width=10)
        mode_menu.pack(side=tk.LEFT, padx=5)

        # Main Content Frame
        content_frame = tk.Frame(self.root, bg=self.colors["light"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Task Entry Frame
        entry_frame = tk.Frame(content_frame, bg=self.colors["light"])
        entry_frame.pack(fill=tk.X, pady=(0, 10))

        self.task_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 12),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=self.colors["accent"],
            highlightcolor=self.colors["secondary"],
            width=40
        )
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Priority Frame (only for BST)
        self.priority_frame = tk.Frame(entry_frame, bg=self.colors["light"])

        tk.Label(
            self.priority_frame,
            text="Priority:",
            font=("Segoe UI", 10),
            bg=self.colors["light"]
        ).pack(side=tk.LEFT)

        ttk.Spinbox(
            self.priority_frame,
            from_=1,
            to=10,
            textvariable=self.priority_var,
            width=5,
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=5)

        # Add Task Button
        add_btn = tk.Button(
            entry_frame,
            text="Add Task",
            command=self.add_task,
            bg=self.colors["success"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            activebackground=self.colors["success"],
            activeforeground="white"
        )
        add_btn.pack(side=tk.LEFT)

        # Task List Frame
        list_frame = tk.Frame(content_frame, bg=self.colors["light"])
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Task Listbox with Scrollbar
        self.task_list = tk.Listbox(
            list_frame,
            font=("Segoe UI", 12),
            selectbackground=self.colors["accent"],
            selectforeground="white",
            activestyle="none",
            relief=tk.FLAT,
            highlightthickness=0
        )
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_list.yview)

        # Button Frame
        btn_frame = tk.Frame(content_frame, bg=self.colors["light"])
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        # Complete Task Button
        self.complete_btn = tk.Button(
            btn_frame,
            text="Complete Next Task",
            command=self.complete_task,
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=15,
            activebackground=self.colors["secondary"]
        )
        self.complete_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Clear Button
        clear_btn = tk.Button(
            btn_frame,
            text="Clear All",
            command=self.clear_tasks,
            bg=self.colors["danger"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            activebackground="#d32f2f"
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Save Button
        save_btn = tk.Button(
            btn_frame,
            text="Save Tasks",
            command=self.save_tasks,
            bg=self.colors["warning"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15,
            activebackground="#f57c00"
        )
        save_btn.pack(side=tk.LEFT)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready | Tasks: 0 | Mode: Queue")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg=self.colors["dark"],
            fg="white",
            anchor=tk.W,
            padx=10
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Initialize
        self.change_mode()

    def change_mode(self, *args):
        self.current_ds = self.mode_var.get()

        # Update UI based on mode
        if self.current_ds == "BST":
            self.priority_frame.pack(side=tk.LEFT, padx=(10, 0))
            self.complete_btn.config(text="Complete Highest Priority")
        else:
            self.priority_frame.pack_forget()

            if self.current_ds == "Queue":
                self.complete_btn.config(text="Complete Next Task")
            elif self.current_ds == "Stack":
                self.complete_btn.config(text="Complete Last Task")
            elif self.current_ds == "Linked List":
                self.complete_btn.config(text="Complete Selected Task")

        self.update_task_list()
        self.update_status()

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return

        if self.current_ds == "BST":
            priority = self.priority_var.get()
            self.bst.add_task(priority, task)
            messagebox.showinfo("Success", f"Added task with priority {priority}")
        elif self.current_ds == "Linked List":
            self.linked_list.add_task(task)
        else:
            self.ds_map[self.current_ds].add_task(task)

        self.task_entry.delete(0, tk.END)
        self.update_task_list()
        self.update_status()

    def complete_task(self):
        if self.current_ds == "Queue":
            completed = self.queue.complete_task()
        elif self.current_ds == "Stack":
            completed = self.stack.complete_task()
        elif self.current_ds == "Linked List":
            selection = self.task_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a task to complete!")
                return
            completed = self.linked_list.complete_task(selection[0])
        elif self.current_ds == "BST":
            completed = self.bst.complete_highest_priority()

        if completed:
            messagebox.showinfo("Task Completed", f"Completed: {completed}")
            self.update_task_list()
            self.update_status()
        else:
            messagebox.showwarning("Warning", "No tasks to complete!")

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.ds_map[self.current_ds].clear()
            self.update_task_list()
            self.update_status()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)

        if self.current_ds == "BST":
            tasks = self.bst.get_all_tasks()
        else:
            tasks = self.ds_map[self.current_ds].get_all_tasks()

        for task in tasks:
            self.task_list.insert(tk.END, task)

    def update_status(self):
        if self.current_ds == "BST":
            count = len(self.bst.get_all_tasks())
        else:
            count = len(self.ds_map[self.current_ds].get_all_tasks())

        self.status_var.set(f"Ready | Tasks: {count} | Mode: {self.current_ds}")

    def save_tasks(self):
        data = {
            "Queue": self.queue.get_all_tasks(),
            "Stack": {
                "tasks": self.stack.get_all_tasks(),
                "history": self.stack.get_history()
            },
            "LinkedList": self.linked_list.get_all_tasks(),
            "BST": self.bst.get_all_tasks()
        }

        try:
            with open("todo_data.json", "w") as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Tasks saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    def load_tasks(self):
        try:
            with open("todo_data.json", "r") as f:
                data = json.load(f)

            # Load queue tasks
            for task in data.get("Queue", []):
                self.queue.add_task(task)

            # Load stack tasks
            stack_data = data.get("Stack", {})
            for task in stack_data.get("tasks", []):
                self.stack.add_task(task)
            for task in stack_data.get("history", []):
                self.stack.completed_stack.append(task)

            # Load linked list tasks
            for task in data.get("LinkedList", []):
                self.linked_list.add_task(task)

            # Load BST tasks
            for task_str in data.get("BST", []):
                try:
                    priority_str, task = task_str.split(": ", 1)
                    priority = int(priority_str[1:])
                    self.bst.add_task(priority, task)
                except:
                    continue

            self.update_task_list()
            self.update_status()
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()