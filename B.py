class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # минимальная степень дерева
        self.leaf = leaf  # является ли узел листом
        self.keys = []  # ключи узла
        self.children = []  # дочерние узлы

    def __str__(self):
        return f"Keys: {self.keys}, Children: {len(self.children)}"

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    # ищет ключ в дереве 
    def search(self, k, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return x, i
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])
        
    # основная функция для вставки ключа в дерево 
    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(self.t)
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    # вспомогательная функция для вставки ключа в неполный узел 
    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    # делит полный узел на два неполных и поднимает ключ в родительский узел 
    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(t, y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]

    # основная функция для удаления ключа из дерева 
    def delete(self, k):
        self.delete_recursive(self.root, k)
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(self.t, leaf=True)

    # рекурсивная функция для удаления ключа из поддерева 
    def delete_recursive(self, x, k):
        t = self.t
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if x.leaf:
            if i < len(x.keys) and x.keys[i] == k:
                x.keys.pop(i)
                return True
            return False
        if i < len(x.keys) and x.keys[i] == k:
            return self.delete_internal_node(x, k, i)
        if len(x.children[i].keys) < t:
            self.fill(x, i)
        if len(x.children) > i and len(x.children[i].keys) >= t:
            return self.delete_recursive(x.children[i], k)
        return False

    # удаление ключа из внутреннего узла 
    def delete_internal_node(self, x, k, i):
        t = self.t
        if len(x.children[i].keys) >= t:
            x.keys[i] = self.get_predecessor(x, i)
            self.delete_recursive(x.children[i], x.keys[i])
        elif len(x.children[i + 1].keys) >= t:
            x.keys[i] = self.get_successor(x, i)
            self.delete_recursive(x.children[i + 1], x.keys[i])
        else:
            self.merge(x, i)
            self.delete_recursive(x.children[i], k)
        return True

    # находит предшественника ключа 
    def get_predecessor(self, x, i):
        current = x.children[i]
        while not current.leaf:
            current = current.children[len(current.children) - 1]
        return current.keys[len(current.keys) - 1]

    # находит преемника ключа 
    def get_successor(self, x, i):
        current = x.children[i + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    # заполняет дочерний узел, если в нём меньше t ключей 
    def fill(self, x, i):
        if i != 0 and len(x.children[i - 1].keys) >= self.t:
            self.borrow_from_prev(x, i)
        elif i != len(x.children) - 1 and len(x.children[i + 1].keys) >= self.t:
            self.borrow_from_next(x, i)
        else:
            if i != len(x.children) - 1:
                self.merge(x, i)
            else:
                self.merge(x, i - 1)

    # заимствует ключ у предыдущего дочернего узла 
    def borrow_from_prev(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]
        for j in range(len(child.keys) - 1, -1, -1):
            child.keys.insert(j + 1, child.keys[j])
        if not child.leaf:
            for j in range(len(child.children) - 1, -1, -1):
                child.children.insert(j + 1, child.children[j])
        child.keys[0] = x.keys[i - 1]
        if not child.leaf:
            child.children[0] = sibling.children.pop()
        x.keys[i - 1] = sibling.keys.pop()

    # заимствует ключ у следующего дочернего ключа 
    def borrow_from_next(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        x.keys[i] = sibling.keys.pop(0)

    # объединяет узел с его соседом 
    def merge(self, x, i):
        child = x.children[i]
        sibling = x.children.pop(i + 1)
        t = self.t
        child.keys.append(x.keys.pop(i))
        for j in range(len(sibling.keys)):
            child.keys.append(sibling.keys[j])
        if not child.leaf:
            for j in range(len(sibling.children)):
                child.children.append(sibling.children[j])

    # рекурсивно печатает структуру дерева 
    def print_tree(self, x=None, level=0):
        if x is None:
            x = self.root
        print("Level", level, " ", len(x.keys), ":", x.keys)
        level += 1
        for child in x.children:
            self.print_tree(child, level)


# примеры использования операций B-дерева
# создание B-дерева с минимальной степенью t=3
b_tree = BTree(t=3)

# пример вставки ключей
keys_to_insert = [45, 18, 23, 11, 37, 32, 50, 16, 29, 24, 27, 5, 8, 39, 41, 21, 48, 53]
for key in keys_to_insert:
    b_tree.insert(key)
print("B-дерево после вставки ключей:")
b_tree.print_tree()

# пример поиска ключа
key_to_search = 23
result = b_tree.search(key_to_search)
if result:
    node, index = result
    print(f"\nКлюч {key_to_search} найден в узле с ключами {node.keys} на позиции {index}.")
else:
    print(f"Ключ {key_to_search} не найден в B-дереве.")

# пример удаления ключа
key_to_delete = 23
print(f"\nУдаление ключа {key_to_delete} из B-дерева.")
b_tree.delete(key_to_delete)
print("B-дерево после удаления ключа:")
b_tree.print_tree()
