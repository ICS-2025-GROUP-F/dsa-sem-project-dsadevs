import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App with Stack History")
        self.tasks = {}  # Task ID: Task Name
        self.completed_stack = []  # Stack
        self.task_id = 1

        # --- UI Elements ---
        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_btn = tk.Button(root, text="Add Task", width=15, command=self.add_task)
        self.add_btn.grid(row=0, column=1)

        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10)

        self.complete_btn = tk.Button(root, text="Mark as Completed", width=20, command=self.complete_task)
        self.complete_btn.grid(row=2, column=0, pady=5)

        self.history_btn = tk.Button(root, text="View Completed History", width=20, command=self.show_history)
        self.history_btn.grid(row=2, column=1)

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task_id, task_name in self.tasks.items():
            self.task_listbox.insert(tk.END, f"[{task_id}] {task_name}")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Warning", "Task name cannot be empty.")
            return
        self.tasks[self.task_id] = task_name
        self.task_id += 1
        self.task_entry.delete(0, tk.END)
        self.refresh_listbox()

    def complete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showinfo("Info", "Select a task to mark as completed.")
            return
        task_text = self.task_listbox.get(selected[0])
        task_id = int(task_text.split(']')[0][1:])
        completed_task = self.tasks.pop(task_id)
        self.completed_stack.append(completed_task)  # Stack push
        self.refresh_listbox()
        messagebox.showinfo("Task Completed", f"'{completed_task}' marked as completed.")

    def show_history(self):
        if not self.completed_stack:
            messagebox.showinfo("History", "No completed tasks yet.")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Completed Task History")

        tk.Label(history_window, text="Completed Tasks (Most Recent First):").pack(pady=5)

        for task in reversed(self.completed_stack):  # LIFO
            tk.Label(history_window, text=f"• {task}").pack(anchor="w", padx=10)

# --- Run the app ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()