# класс узла AVL-дерева
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None
        self.height = 1

# вспомогательные функции ждя вычисления высоты и баланса 
def get_height(node):
    if not node:
        return 0
    return node.height 

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right) 

# правый поворот для балансировки 
def right_rotate(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    return x

# левый поворот для балансировки 
def left_rotate(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    return y

# большое правое вращение (левый-правый случай)
def double_right_rotate(node):
    node.left = left_rotate(node.left)
    return right_rotate(node)

# большое левое вращение (правый-левый случай)
def double_left_rotate(node):
    node.right = right_rotate(node.right)
    return left_rotate(node)

# вставка узла 
def insert(node, key):
    if not node:
        return AVLNode(key)
    elif key < node.key:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    node.height = 1 + max(get_height(node.left), get_height(node.right))
    balance = get_balance(node)

    # балансировка
    if balance > 1 and key < node.left.key:
        return right_rotate(node)
    if balance < -1 and key > node.right.key:
        return left_rotate(node)
    if balance > 1 and key > node.left.key:
        return double_right_rotate(node)  # вызов операции большого правого вращения
    if balance < -1 and key < node.right.key:
        return double_left_rotate(node)  # вызов операции большого левого вращения

    return node

# нахождение узла с минимальным ключом 
def min_value_node(node):
    while node.left:
        node = node.left
    return node

# удаление узла 
def delete_node(root, key):
    if not root:
        return root
    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if not root.left or not root.right:
            root = root.left or root.right
        else:
            temp = min_value_node(root.right)
            root.key, root.right = temp.key, delete_node(root.right, temp.key)
    if not root:
        return root
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    balance = get_balance(root)
    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)
    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)
    return root

# прямой обход дерева (выводит значения узлов в порядке "корень, левое поддерево, правое поддерево")
def pre_order_traversal(node):
    if node:
        print(f"{node.key} ", end="")
        pre_order_traversal(node.left)
        pre_order_traversal(node.right)

# пример использования
root = None
for key in [50, 30, 20, 40, 70, 60, 80]:
    root = insert(root, key)
print("Прямой обход дерева после вставки новых узлов:")
pre_order_traversal(root)
print()

root = delete_node(root, 40)
print("\nПрямой обход дерева после удаления узла:")
pre_order_traversal(root)
print()

