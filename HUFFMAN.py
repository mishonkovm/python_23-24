import heapq # модуль для обработки бинарных куч (помогают быстро находить и удалять наименьший элемент)
from collections import Counter # класс для подсчёта частоты элементов в итерируемом объекте; 
                                # создаёт словарь, где кдючами являются элементы, а значениями - их частоты

class HuffmanNode:
    def __init__(self, frequency, symbol=None, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other): # определяем поведение оператора "меньше" для объектов класса (очередь с приоритетом)
        return self.frequency < other.frequency

# построение дерева Хаффмана из частот символов, используя очередь с приоритетом
def build_huffman_tree(frequencies):
    priority_queue = [HuffmanNode(freq, symbol) for symbol, freq in frequencies.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(left.frequency + right.frequency, left=left, right=right)
        heapq.heappush(priority_queue, merged)
    
    return heapq.heappop(priority_queue)

# рекурсивная функция для генерации кодов Хаффмана, проходя по дереву 
def generate_huffman_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
        generate_huffman_codes(node.left, prefix + "0", codebook)
        generate_huffman_codes(node.right, prefix + "1", codebook)
    return codebook

# основная функция для кодирования строки, возвращающая закодированные данные и таблицу кодов 
def huffman_encoding(data):
    if not data:
        return "", {}
    
    frequency = Counter(data)
    huffman_tree = build_huffman_tree(frequency)
    huffman_codes = generate_huffman_codes(huffman_tree)
    encoded_data = "".join(huffman_codes[symbol] for symbol in data)
    
    return encoded_data, huffman_codes

# функция для декодирования строки, используя таблицу кодов
def huffman_decoding(encoded_data, huffman_codes):
    reverse_codebook = {code: symbol for symbol, code in huffman_codes.items()}
    current_code = ""
    decoded_data = []
    
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codebook:
            decoded_data.append(reverse_codebook[current_code])
            current_code = ""
    
    return "".join(decoded_data)

# пример использования
if __name__ == "__main__":
    data = "Я изучаю алгоритм Хаффмана"
    print("Исходные данные:", data)

    encoded_data, huffman_codes = huffman_encoding(data)
    print("\nЗакодированные данные:", encoded_data)
    print("Коды Хаффмана:", huffman_codes)

    decoded_data = huffman_decoding(encoded_data, huffman_codes)
    print("\nДекодированные данные:", decoded_data)
