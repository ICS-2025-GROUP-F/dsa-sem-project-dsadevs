class TaskNode:
    def __init__(self, task):  # Fixed: double underscores
        self.task = task
        # Below are pointers
        self.next = None
        self.prev = None


class TaskLinkedList:
    def __init__(self):  # Fixed: double underscores
        # Tasks
        self.head = None
        self.tail = None
        self.size = 0

    def add_task(self, task, position=None):
        # Add task at end or any chosen position
        new_node = TaskNode(task)
        # Empty list
        if not self.head:
            self.head = self.tail = new_node
        elif position == 0:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        elif position is None or position >= self.size:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                current = current.next
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node
        self.size += 1

    def delete_task(self, position):
        # Deleting tasks
        if position < 0 or position >= self.size:
            raise IndexError("Invalid position")
        if self.size == 1:
            self.head = self.tail = None
        elif position == 0:
            self.head = self.head.next
            self.head.prev = None
        elif position == self.size - 1:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            current = self.head
            for _ in range(position):
                current = current.next
            current.prev.next = current.next
            current.next.prev = current.prev
        self.size -= 1

    def move_task(self, from_pos, to_pos):
        # Moving tasks from one node to another
        if from_pos == to_pos:
            return
        current = self.head
        for _ in range(from_pos):
            current = current.next
        moved_task = current.task  # Save the task before deletion
        self.delete_task(from_pos)
        self.add_task(moved_task, to_pos)  # Use the saved task

    def display_tasks(self):
        # Printing Tasks
        current = self.head
        while current:
            print(current.task)
            current = current.next


# Demonstration of how to use the class
if __name__ == "__main__":
    task_list = TaskLinkedList()
    task_list.add_task("Task 1")
    task_list.add_task("Task 2")
    task_list.add_task("Task 3")
    task_list.add_task("Task 4", 1)  # Insert at position 1

    print("Initial tasks:")
    task_list.display_tasks()

    print("\nMoving task 2 to the end:")
    task_list.move_task(1, 3)
    task_list.display_tasks()

    print("\nDeleting task at position 1:")
    task_list.delete_task(1)
    task_list.display_tasks()