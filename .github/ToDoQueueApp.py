# Import necessary modules
import tkinter as tk                         # GUI toolkit
from tkinter import messagebox, ttk          # Message boxes and themed widgets
from collections import deque  # Deque is used for efficient queue operations
import os

class ToDoQueueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Queue-Based To-Do App")   # Title of the window
        self.root.geometry("600x400")              # Set window size

        # Initialize an empty deque to act as a task queue
        self.task_queue = deque()

        # Create all user interface components
        self.setup_ui()

        # Load previously saved tasks from file (if any)
        self.load_tasks()

    def setup_ui(self):
        # === Entry Frame ===
        entry_frame = tk.Frame(self.root)
        entry_frame.pack(pady=10)

        # Task entry input field
        self.task_entry = tk.Entry(entry_frame, width=40, font=('Arial', 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)

        # Pressing Enter also adds a task
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # Add Task button
        add_button = tk.Button(entry_frame, text="Add Task", command=self.add_task, bg='#4CAF50', fg='white')
        add_button.pack(side=tk.LEFT, padx=5)

        # === Control Frame ===
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=5)

        # Complete next task (dequeue from queue)
        complete_button = tk.Button(control_frame, text="Complete Next Task", command=self.complete_task, bg='#2196F3',
                                    fg='white')
        complete_button.pack(side=tk.LEFT, padx=5)

        # Clear all tasks
        clear_button = tk.Button(control_frame, text="Clear All", command=self.clear_tasks, bg='#f44336', fg='white')
        clear_button.pack(side=tk.LEFT, padx=5)

        # Save tasks to file
        save_button = tk.Button(control_frame, text="Save Tasks", command=self.save_tasks, bg='#FFC107', fg='black')
        save_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(control_frame, text="Delete Saved Tasks", command=self.delete_saved_tasks,bg='#9C27B0', fg='white')
        delete_button.pack(side=tk.LEFT, padx=5)

        # Listbox to show tasks
        self.task_listbox = tk.Listbox(self.root, width=60, height=15, font=('Arial', 12), selectbackground='#a6a6a6')
        self.task_listbox.pack(pady=10)

        # Label showing current number of tasks
        self.status_label = tk.Label(self.root, text="Tasks in queue: 0", font=('Arial', 10))
        self.status_label.pack()

    def add_task(self):
        task = self.task_entry.get().strip()  # Get input and remove leading/trailing spaces
        if task:
            self.task_queue.append(task)  # Enqueue the task
            self.update_task_list()  # Refresh listbox
            self.task_entry.delete(0, tk.END)  # Clear input field
            self.update_status()  # Update task count
        else:
            messagebox.showwarning("Warning", "Please enter a task description.")

    def complete_task(self):
        if self.task_queue:
            # Dequeue the task (remove from the front of the queue)
            completed_task = self.task_queue.popleft()
            self.update_task_list()
            self.update_status()
            messagebox.showinfo("Task Completed", f"You completed: {completed_task}")
        else:
            messagebox.showwarning("Warning", "No tasks in the queue!")

    def clear_tasks(self):
        if self.task_queue:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
                self.task_queue.clear()
                self.update_task_list()
                self.update_status()
        else:
            messagebox.showwarning("Warning", "The task queue is already empty!")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.task_queue:
            self.task_listbox.insert(tk.END, task)

    def update_status(self):
        count = len(self.task_queue)
        self.status_label.config(text=f"Tasks in queue: {count}")

    def save_tasks(self):
        if not self.task_queue:
            messagebox.showwarning("Warning", "There are no tasks to save.")
            return
        try:
            with open("tasks.txt", "w") as f:
                for task in self.task_queue:
                    f.write(task + "\n")
            messagebox.showinfo("Success", "Tasks saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                for line in f:
                    task = line.strip()
                    if task:
                        self.task_queue.append(task)
            self.update_task_list()
            self.update_status()
        except FileNotFoundError:
            pass  # No saved tasks file yet
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")

    def delete_saved_tasks(self):
        if os.path.exists("tasks.txt"):
            try:
                os.remove("tasks.txt")  # Deletes the file
                messagebox.showinfo("Deleted", "Saved tasks have been deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete saved tasks: {str(e)}")
        else:
            messagebox.showinfo("Info", "No saved tasks file found.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoQueueApp(root)
    root.mainloop()