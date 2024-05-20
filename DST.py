class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# реализует методы вставки, поиска и удаления узлов 
class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._minValueNode(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        return node

    def _minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorderTraversal(self): # используем для получения элементов дерева в порядке возрастания 
        result = []
        self._inorderTraversal(self.root, result)
        return result

    def _inorderTraversal(self, node, result):
        if node:
            self._inorderTraversal(node.left, result)
            result.append(node.key)
            self._inorderTraversal(node.right, result)


bst = BinarySearchTree()

# вставка ключей
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)
bst.insert(60)
bst.insert(80)

# поиск ключа
print("Поиск 40:", bst.search(40) is not None)
print("Поиск 100:", bst.search(100) is not None)

# удаление ключа
bst.delete(20)
bst.delete(30)
bst.delete(50)

# печать дерева в порядке возрастания
print("Симметричный обход дерева:", bst.inorderTraversal())
