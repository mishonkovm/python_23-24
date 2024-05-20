# Алгоритм Бойера-Мура 

# создаёт таблицу "плохих символов", которая указывает на последнее вхождение каждого символа в шаблоне
def bad_character_heuristic(pattern):
    alphabet_size = 256
    pattern_length = len(pattern)
    bad_char = [-1] * alphabet_size

    for i in range(pattern_length):
        bad_char[ord(pattern[i])] = i

    return bad_char

# функция для поиска вхождений подстроки в тексте 
def boyer_moore(text, pattern):
    text_length = len(text)
    pattern_length = len(pattern)
    bad_char = bad_character_heuristic(pattern)
    shift = 0

    while shift <= text_length - pattern_length:
        j = pattern_length - 1

        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            print("Найдено вхождение подстроки на позиции", shift)
            shift += (pattern_length - bad_char[ord(text[shift + pattern_length])] if shift + pattern_length < text_length else 1)
        else:
            shift += max(1, j - bad_char[ord(text[shift + j])] if bad_char[ord(text[shift + j])] != -1 else 1)

# пример
text = "I love playing guitar"
pattern = "love"
boyer_moore(text, pattern)
