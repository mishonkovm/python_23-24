class Node:
    def __init__(self, data, color="red"):
        self.data = data
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0)
        self.TNULL.color = "black"
        self.root = self.TNULL

    # выполняет левый поворот вокруг узла x  
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # выполняет правый поворот вокруг узла x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # восстанавливает свойства красно-чёрного дерева после вставки нового узла 
    def insert_fix(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    # вставляет новый узел с заданным ключом в дерево, затем вызывает функцию для восстановления свойств красно-чёрного дерева 
    def insert(self, key):
        node = Node(key)
        node.parent = None
        node.data = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "red"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = "black"
            return

        if node.parent.parent == None:
            return

        self.insert_fix(node)

    # восстанавливает свойства красно-чёрного дерева после удаления узла 
    def delete_fix(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    # заменяет одно поддерево другим 
    def transplant_subtree(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # удаляет узел с заданным ключом из дерева, определяет узел для удаления и вызывает функцию для восстановления свойств дерева после удаления
    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node
            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.transplant_subtree(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.transplant_subtree(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant_subtree(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant_subtree(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self.delete_fix(x)

    # удаляет узел с заданным значением из дерева 
    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    # рекурсивная функция для печати структуры дерева 
    def print_tree_helper(self, node, indent, last):
        if node != self.TNULL:
            print(indent, end=' ')
            if last:
                print("R----", end=' ')
                indent += "   "
            else:
                print("L----", end=' ')
                indent += "|  "

            s_color = "RED" if node.color == "red" else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.print_tree_helper(node.left, indent, False)
            self.print_tree_helper(node.right, indent, True)

    def print_tree(self):
        self.print_tree_helper(self.root, "", True)

    # находит узел с минимальным значением в поддереве, начиная с заданного узла 
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    # находит узел с максимальным значением в поддереве, начиная с заданного узла 
    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    # ищет узел с заданным значением в дереве 
    def search_tree(self, k):
        return self.search_tree_helper(self.root, k)

    # ищет узел с заданным значением в дереве 
    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

# cоздание экземпляра красно-чёрного дерева
rb_tree = RedBlackTree()

# вставка узлов
rb_tree.insert(10)
rb_tree.insert(20)
rb_tree.insert(5)
rb_tree.insert(30)
rb_tree.insert(15)
rb_tree.insert(25)

print("Красно-Черное Дерево после вставки:")
rb_tree.print_tree()

# поиск узла
search_result = rb_tree.search_tree(20)
if search_result != rb_tree.TNULL:
    print("\nУзел 20 найден в дереве.")
else:
    print("Узел 20 не найден в дереве.")

# удаление узла
rb_tree.delete_node(20)
print("\nКрасно-Черное Дерево после удаления узла 20:")
rb_tree.print_tree()

# нахождение минимального и максимального узлов
min_node = rb_tree.minimum(rb_tree.root)
max_node = rb_tree.maximum(rb_tree.root)
print("\nМинимальный узел в дереве:", min_node.data)
print("Максимальный узел в дереве:", max_node.data)
