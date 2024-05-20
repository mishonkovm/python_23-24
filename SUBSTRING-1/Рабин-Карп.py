# Алгоритм Рабина-Карпа 

def build_transition_table(pattern):
    d = 256  # размер алфавита (ASCII символов)
    q = 101  # простое число для хеширования
    m = len(pattern)
    h = pow(d, m-1) % q
    p = 0  # хеш для подстроки

    # вычисление хеша для подстроки
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q

    return p, h, q, d

def finite_automaton_matcher(text, pattern):
    n = len(text)
    m = len(pattern)
    p, h, q, d = build_transition_table(pattern)
    t = 0  # хеш для текста

    # вычисление хеша для первой подстроки текста
    for i in range(m):
        t = (d * t + ord(text[i])) % q

    # поиск вхождений
    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if pattern[j] != text[i + j]:
                    match = False
                    break
            if match:
                print("Найдено вхождение подстроки на позиции", i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q

# пример
text = "ilikelearningmathematics"
pattern = "like"
finite_automaton_matcher(text, pattern)



