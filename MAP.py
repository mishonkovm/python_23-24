class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    DELETED = object()  # специальный маркер для удаления

    def __init__(self, size=10, collision_resolution='chaining', load_factor=0.7):
        self.size = size # размер таблицы хеширования
        self.table = [None] * size # инициализация таблицы
        self.collision_resolution = collision_resolution # метод разрешения коллизий
        self.load_factor = load_factor # порог заполнения

        if collision_resolution not in ['chaining', 'open_addressing']:
            raise ValueError("Неподдерживаемый метод разрешения коллизий")

    # хеш-функция для вычисления индекса
    def _hash(self, key):
        return hash(key) % self.size
    # поиск слота для ключа (для метода открытой адресации)
    def _find_slot(self, key, for_insert=False):
        index = self._hash(key)
        start_index = index
        skipped = False
        
        while self.table[index] is not None and self.table[index] != self.DELETED:
            if self.table[index][0] == key:
                return index
            if not skipped and self.table[index][0] == self.DELETED:
                skipped = True
            index = (index + 1) % self.size
            if index == start_index:
                if for_insert:
                    self._resize()
                    return self._find_slot(key, for_insert=True)
                raise Exception("Хеш-таблица заполнена")

        return index if for_insert else None

    # изменение размера таблицы при переполнении
    def _resize(self):
        new_size = self.size * 2
        new_table = [None] * new_size
        for item in self.table:
            if item is not None and item != self.DELETED:
                key, value = item
                index = hash(key) % new_size
                while new_table[index] is not None:
                    index = (index + 1) % new_size
                new_table[index] = (key, value)
        self.table = new_table
        self.size = new_size

    #  вставка пары ключ-значение в хеш-таблицу
    def put(self, key, value):
        if not isinstance(key, (int, str)):
            raise TypeError("Ключ должен быть строкой или целым числом")
        if self.collision_resolution == 'chaining':
            index = self._hash(key)
            if self.table[index] is None:
                self.table[index] = Node(key, value)
            else:
                current = self.table[index]
                while current:
                    if current.key == key:
                        current.value = value
                        return
                    if current.next is None:
                        break
                    current = current.next
                current.next = Node(key, value)

        elif self.collision_resolution == 'open_addressing':
            index = self._find_slot(key, for_insert=True)
            self.table[index] = (key, value)

    #  получение значения по ключу
    def get(self, key):
        if not isinstance(key, (int, str)):
            raise TypeError("Ключ должен быть строкой или целым числом")
        if self.collision_resolution == 'chaining':
            index = self._hash(key)
            current = self.table[index]
            while current:
                if current.key == key:
                    return current.value
                current = current.next
            return None

        elif self.collision_resolution == 'open_addressing':
            index = self._find_slot(key)
            return self.table[index][1] if index is not None else None
        
    #  удаление элемента по ключу
    def remove(self, key):
        if not isinstance(key, (int, str)):
            raise TypeError("Ключ должен быть строкой или целым числом")
        if self.collision_resolution == 'chaining':
            index = self._hash(key)
            current = self.table[index]
            prev = None
            while current:
                if current.key == key:
                    if prev:
                        prev.next = current.next
                    else:
                        self.table[index] = current.next
                    return
                prev = current
                current = current.next

        elif self.collision_resolution == 'open_addressing':
            index = self._find_slot(key)
            if index is not None:
                self.table[index] = self.DELETED

# пример использования
if __name__ == "__main__":
    
    # пример с методом цепочек
    print("Метод цепочек:")
    map_chaining = HashMap(size=5, collision_resolution='chaining')
    map_chaining.put("key1", "value1")
    map_chaining.put("key2", "value2")
    map_chaining.put("key3", "value3")
    map_chaining.put("key4", "value4")
    map_chaining.put("key5", "value5")
    
    print(map_chaining.get("key1"))  
    print(map_chaining.get("key2"))  
    print(map_chaining.get("key3"))  
    print(map_chaining.get("key4"))  
    print(map_chaining.get("key5"))  

    map_chaining.remove("key3")
    print(map_chaining.get("key3")) # вывод: None

    # пример с открытой адресацией
    print("\nОткрытая адресация:")
    map_open_addressing = HashMap(size=5, collision_resolution='open_addressing')
    map_open_addressing.put("key1", "value1")
    map_open_addressing.put("key2", "value2")
    map_open_addressing.put("key3", "value3")
    map_open_addressing.put("key4", "value4")
    map_open_addressing.put("key5", "value5")
    
    print(map_open_addressing.get("key1"))  
    print(map_open_addressing.get("key2"))  
    print(map_open_addressing.get("key3"))  
    print(map_open_addressing.get("key4"))  
    print(map_open_addressing.get("key5"))  

    map_open_addressing.remove("key3")
    print(map_open_addressing.get("key3")) # вывод: None

    # добавление новых элементов после удаления
    map_open_addressing.put("key6", "value6")
    map_open_addressing.put("key7", "value7")
    
    print(map_open_addressing.get("key6"))  
    print(map_open_addressing.get("key7"))  

