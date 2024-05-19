class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    # добавляет слово в дерево, создавая узлы по мере необходимости 
    def insert(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    # ищет слово в дереве, возвращая True, если слово найдено, и False в противном случае 
    def search(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    # удаляет слово из дерева, удаляя узлы, если они больше не являются частью других слов 
    def delete(self, key):
        def _delete(node, key, depth):
            if node is None:
                return False
            
            if depth == len(key):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0
            
            char = key[depth]
            if char not in node.children:
                return False
            
            should_delete_child = _delete(node.children[char], key, depth + 1)
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0
            
            return False
        
        _delete(self.root, key, 0)
    
    # рекурсивно собирает и возвращает все слова в дереве 
    def display(self):
        words = []
        
        def _display(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)
            for char, child_node in node.children.items():
                _display(child_node, current_word + char)
        
        _display(self.root, "")
        return words

trie = Trie()

# добавление ключей
trie.insert("school")
trie.insert("world")
trie.insert("university")
trie.insert("student")

print("Слова в Trie после добавления ключей:")
print(trie.display())

# поиск ключей
print("\nПоиск ключей:")
print(f"Поиск 'school': {trie.search('school')}")
print(f"Поиск 'world': {trie.search('world')}")
print(f"Поиск 'university': {trie.search('university')}")
print(f"Поиск 'student': {trie.search('student')}")
print(f"Поиск 'teacher': {trie.search('teacher')}")

# удаление ключа
trie.delete("world")
print("\nСлова в Trie после удаления 'world':")
print(trie.display())

trie.delete("school")
print("\nСлова в Trie после удаления 'school':")
print(trie.display())

print("\nПоиск ключей после удаления:")
print(f"Поиск 'school': {trie.search('school')}")
print(f"Поиск 'world': {trie.search('world')}")
print(f"Поиск 'university': {trie.search('university')}")
print(f"Поиск 'student': {trie.search('student')}")
