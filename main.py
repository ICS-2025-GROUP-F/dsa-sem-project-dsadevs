import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import json


class QueueToDo:
    def __init__(self):
        self.tasks = deque()

    def add_task(self, task):
        self.tasks.append(task)

    def complete_task(self):
        return self.tasks.popleft() if self.tasks else None

    def get_all_tasks(self):
        return list(self.tasks)

    def remove_task(self, task):
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

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

    def undo_completion(self):
        if self.completed_stack:
            task = self.completed_stack.pop()
            self.tasks.append(task)
            return task
        return None

    def get_all_tasks(self):
        return self.tasks.copy()

    def get_history(self):
        return self.completed_stack.copy()

    def remove_task(self, task):
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

    def clear(self):
        self.tasks.clear()
        self.completed_stack.clear()


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

    def remove_task(self, task):
        if not self.head:
            return False

        if self.head.task == task:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.task == task:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

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
        self.completed_tasks = []

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
        self.completed_tasks.append(current.task)
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

    def remove_task(self, task):
        all_tasks = self.get_all_tasks()
        new_tasks = [t for t in all_tasks if not t.endswith(task)]

        self.root = None
        for task_str in new_tasks:
            try:
                priority_str, task_content = task_str.split(": ", 1)
                priority = int(priority_str[1:])
                self.add_task(priority, task_content)
            except:
                continue
        return task in [t.split(": ", 1)[1] for t in all_tasks]

    def clear(self):
        self.root = None
        self.completed_tasks = []


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Structures To-Do App")
        self.root.geometry("1000x750")
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

        # Global history tracking
        self.completed_history = []

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

        # Priority Frame (for BST)
        self.priority_frame = tk.Frame(entry_frame, bg=self.colors["light"])
        self.priority_frame.pack(side=tk.LEFT, padx=(10, 0))

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

        # DS Operations Frame
        ds_ops_frame = tk.Frame(content_frame, bg=self.colors["light"])
        ds_ops_frame.pack(fill=tk.X, pady=(10, 0))

        # Queue Operations
        queue_frame = tk.LabelFrame(ds_ops_frame, text="Queue Operations", bg=self.colors["light"], padx=5, pady=5)
        queue_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            queue_frame,
            text="Complete Next (FIFO)",
            command=self.complete_queue_task,
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        # Stack Operations
        stack_frame = tk.LabelFrame(ds_ops_frame, text="Stack Operations", bg=self.colors["light"], padx=5, pady=5)
        stack_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            stack_frame,
            text="Complete Task (LIFO)",
            command=self.complete_stack_task,
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            stack_frame,
            text="Show History",
            command=self.show_history,
            bg=self.colors["secondary"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            stack_frame,
            text="Undo Completion",
            command=self.undo_completion,
            bg=self.colors["warning"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        # Linked List Operations
        ll_frame = tk.LabelFrame(ds_ops_frame, text="Linked List Operations", bg=self.colors["light"], padx=5, pady=5)
        ll_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            ll_frame,
            text="Complete Selected",
            command=self.complete_linked_list_task,
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        # BST Operations
        bst_frame = tk.LabelFrame(ds_ops_frame, text="BST Operations", bg=self.colors["light"], padx=5, pady=5)
        bst_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(
            bst_frame,
            text="Complete Highest Priority",
            command=self.complete_bst_task,
            bg=self.colors["primary"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10
        ).pack(side=tk.LEFT, padx=5)

        # Common Operations Frame
        common_ops_frame = tk.Frame(content_frame, bg=self.colors["light"])
        common_ops_frame.pack(fill=tk.X, pady=(10, 0))

        # Clear Button
        clear_btn = tk.Button(
            common_ops_frame,
            text="Clear All Tasks",
            command=self.clear_tasks,
            bg=self.colors["danger"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Save Button
        save_btn = tk.Button(
            common_ops_frame,
            text="Save Tasks",
            command=self.save_tasks,
            bg=self.colors["warning"],
            fg="white",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=15
        )
        save_btn.pack(side=tk.LEFT)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready | Tasks: 0")
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

    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task description!")
            return

        # Add to all data structures
        self.queue.add_task(task)
        self.stack.add_task(task)
        self.linked_list.add_task(task)

        # For BST, use the priority value
        priority = self.priority_var.get()
        self.bst.add_task(priority, task)

        self.task_entry.delete(0, tk.END)
        self.update_task_list()
        self.update_status()
        messagebox.showinfo("Success", "Task added to all data structures!")

    def complete_queue_task(self):
        completed = self.queue.complete_task()
        if completed:
            # Remove from other data structures
            self.stack.remove_task(completed)
            self.linked_list.remove_task(completed)
            self.bst.remove_task(completed)

            # Add to global history
            self.completed_history.append(("Queue", completed))

            messagebox.showinfo("Queue Task Completed", f"Completed (FIFO): {completed}")
            self.update_task_list()
            self.update_status()
        else:
            messagebox.showwarning("Warning", "No tasks in queue to complete!")

    def complete_stack_task(self):
        completed = self.stack.complete_task()
        if completed:
            # Remove from other data structures
            self.queue.remove_task(completed)
            self.linked_list.remove_task(completed)
            self.bst.remove_task(completed)

            # Add to global history
            self.completed_history.append(("Stack", completed))

            messagebox.showinfo("Stack Task Completed", f"Completed (LIFO): {completed}")
            self.update_task_list()
            self.update_status()
        else:
            messagebox.showwarning("Warning", "No tasks in stack to complete!")

    def complete_linked_list_task(self):
        selection = self.task_list.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task to complete!")
            return

        task = self.task_list.get(selection[0])
        if task.startswith("P") and ": " in task:
            task = task.split(": ", 1)[1]

        completed = None
        if task in self.queue.get_all_tasks():
            completed = task
            self.queue.remove_task(task)
        if self.stack.remove_task(task):
            completed = task
        if self.linked_list.remove_task(task):
            completed = task
        if self.bst.remove_task(task):
            completed = task

        if completed:
            # Add to global history
            self.completed_history.append(("Linked List", completed))

            messagebox.showinfo("Task Completed", f"Completed: {completed}")
            self.update_task_list()
            self.update_status()
        else:
            messagebox.showwarning("Warning", "Could not complete the selected task!")

    def complete_bst_task(self):
        completed = self.bst.complete_highest_priority()
        if completed:
            # Remove from other data structures
            self.queue.remove_task(completed)
            self.stack.remove_task(completed)
            self.linked_list.remove_task(completed)

            # Add to global history
            self.completed_history.append(("BST", completed))

            messagebox.showinfo("BST Task Completed", f"Completed (Highest Priority): {completed}")
            self.update_task_list()
            self.update_status()
        else:
            messagebox.showwarning("Warning", "No tasks in BST to complete!")

    def show_history(self):
        if not self.completed_history:
            messagebox.showinfo("Completion History", "No completed tasks in history!")
            return

        history_text = "Completion History:\n\n" + "\n".join(
            f"{i + 1}. {task} (via {method})"
            for i, (method, task) in enumerate(reversed(self.completed_history)))
        messagebox.showinfo("Completion History", history_text)

    def undo_completion(self):
        if not self.completed_history:
            messagebox.showwarning("Cannot Undo", "No completed tasks to undo!")
            return

        method, undone_task = self.completed_history.pop()

        # Add back to all data structures
        self.queue.add_task(undone_task)
        self.stack.add_task(undone_task)
        self.linked_list.add_task(undone_task)

        # For BST, use current priority value
        self.bst.add_task(self.priority_var.get(), undone_task)

        messagebox.showinfo("Undo Successful", f"Task restored: {undone_task} (originally completed via {method})")
        self.update_task_list()
        self.update_status()

    def clear_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.queue.clear()
            self.stack.clear()
            self.linked_list.clear()
            self.bst.clear()
            self.completed_history.clear()
            self.update_task_list()
            self.update_status()

    def update_task_list(self):
        self.task_list.delete(0, tk.END)

        # Get tasks from all structures and combine them
        queue_tasks = self.queue.get_all_tasks()
        stack_tasks = self.stack.get_all_tasks()
        ll_tasks = self.linked_list.get_all_tasks()
        bst_tasks = self.bst.get_all_tasks()

        # Create a unified list (prioritizing BST tasks first since they have priority info)
        all_tasks = []

        # Add BST tasks first (they have priority info)
        all_tasks.extend(bst_tasks)

        # Add other tasks, avoiding duplicates
        for task in queue_tasks + stack_tasks + ll_tasks:
            if task not in [t.split(": ", 1)[-1] for t in all_tasks]:
                all_tasks.append(task)

        for task in all_tasks:
            self.task_list.insert(tk.END, task)

    def update_status(self):
        # Count unique tasks across all data structures
        queue_tasks = set(self.queue.get_all_tasks())
        stack_tasks = set(self.stack.get_all_tasks())
        ll_tasks = set(self.linked_list.get_all_tasks())
        bst_tasks = set(t.split(": ", 1)[-1] for t in self.bst.get_all_tasks())

        unique_tasks = queue_tasks.union(stack_tasks).union(ll_tasks).union(bst_tasks)
        count = len(unique_tasks)

        self.status_var.set(f"Ready | Tasks: {count}")

    def save_tasks(self):
        data = {
            "Queue": self.queue.get_all_tasks(),
            "Stack": {
                "tasks": self.stack.get_all_tasks(),
                "history": self.stack.get_history()
            },
            "LinkedList": self.linked_list.get_all_tasks(),
            "BST": self.bst.get_all_tasks(),
            "BST_Completed": getattr(self.bst, 'completed_tasks', []),
            "Global_History": self.completed_history
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
                self.stack.add_task(task)
                self.linked_list.add_task(task)

            # Load stack history
            stack_data = data.get("Stack", {})
            for task in stack_data.get("history", []):
                self.stack.completed_stack.append(task)

            # Load BST tasks
            for task_str in data.get("BST", []):
                try:
                    priority_str, task = task_str.split(": ", 1)
                    priority = int(priority_str[1:])
                    self.bst.add_task(priority, task)
                except:
                    continue

            # Load BST completed tasks
            for task in data.get("BST_Completed", []):
                if hasattr(self.bst, 'completed_tasks'):
                    self.bst.completed_tasks.append(task)

            # Load global history
            self.completed_history = data.get("Global_History", [])

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