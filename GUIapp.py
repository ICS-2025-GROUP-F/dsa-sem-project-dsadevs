import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from TaskBST import TaskBST

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List - BST Sorted")

        self.sort_method = tk.StringVar(value="due_date")
        self.bst = TaskBST()
        self.tasks = []

        self.setup_ui()

    def setup_ui(self):
        # Sorting Choice
        sort_frame = tk.Frame(self.root)
        sort_frame.grid(row=0, column=0, columnspan=2)
        tk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT)
        tk.OptionMenu(sort_frame, self.sort_method, "due_date", "title", "priority").pack(side=tk.LEFT)

        # Task Input
        tk.Label(self.root, text="Title").grid(row=1, column=0)
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Description").grid(row=2, column=0)
        self.desc_entry = tk.Entry(self.root)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Due Date (YYYY-MM-DD)").grid(row=3, column=0)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Priority").grid(row=4, column=0)
        self.priority_entry = tk.Entry(self.root)
        self.priority_entry.grid(row=4, column=1)

        # Buttons
        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=5, column=0)
        tk.Button(self.root, text="Delete Selected", command=self.delete_task).grid(row=5, column=1)

        # TreeView
        self.tree = ttk.Treeview(self.root, columns=("Title", "Due Date", "Priority"), show="headings")
        for col in ("Title", "Due Date", "Priority"):
            self.tree.heading(col, text=col)
        self.tree.grid(row=6, column=0, columnspan=2)

    def add_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due_str = self.date_entry.get()
        priority = self.priority_entry.get()

        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid date", "Use format YYYY-MM-DD")
            return

        task = {'title': title, 'description': desc, 'due_date': due_date, 'priority': priority}
        self.tasks.append(task)
        self.refresh_bst()
        self.refresh_tree()

    def refresh_bst(self):
        self.bst = TaskBST()
        for task in self.tasks:
            key = self.get_sort_key(task)
            self.bst.insert(key, task)

    def get_sort_key(self, task):
        sort_by = self.sort_method.get()
        if sort_by == "due_date":
            return task['due_date']
        elif sort_by == "title":
            return task['title'].lower()
        elif sort_by == "priority":
            return int(task['priority']) if task['priority'].isdigit() else 0
        return task['due_date']

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for key, task in self.bst.inorder():
            self.tree.insert('', 'end', values=(task['title'], task['due_date'].strftime("%Y-%m-%d"), task['priority']))

    def delete_task(self):
        selected = self.tree.focus()
        if not selected:
            return
        title = self.tree.item(selected)['values'][0]
        self.tasks = [t for t in self.tasks if t['title'] != title]
        self.refresh_bst()
        self.refresh_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
