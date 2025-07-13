class Node:
    def __init__(self, key, task):
        self.key = key
        self.task = task
        self.left = None
        self.right = None

class TaskBST:
    def __init__(self):
        self.root = None

    def insert(self, key, task):
        def _insert(node, key, task):
            if not node:
                return Node(key, task)
            if key < node.key:
                node.left = _insert(node.left, key, task)
            else:
                node.right = _insert(node.right, key, task)
            return node
        self.root = _insert(self.root, key, task)

    def inorder(self):
        tasks = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                tasks.append((node.key, node.task))
                _inorder(node.right)
        _inorder(self.root)
        return tasks

    def delete(self, key):
        def _min_value_node(node):
            while node.left:
                node = node.left
            return node

        def _delete(node, key):
            if not node:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                temp = _min_value_node(node.right)
                node.key, node.task = temp.key, temp.task
                node.right = _delete(node.right, temp.key)
            return node

        self.root = _delete(self.root, key)
