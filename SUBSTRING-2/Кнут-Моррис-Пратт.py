# Алгоритм Кнута-Морриса-Пратта

# вычисляет префикс-функцию для шаблона 
def compute_prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0

    for q in range(1, m):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
        pi[q] = k
    return pi

# осуществляет поиск вхождений шаблона в тексте с использованием префикс-функции
def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    pi = compute_prefix_function(pattern)
    q = 0
    occurrences = []

    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = pi[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            occurrences.append(i - m + 1)
            q = pi[q - 1]
    return occurrences

# пример
text = "Мама мыла раму"
pattern = "раму"
occurrences = kmp_search(text, pattern)
if occurrences:
    print("Найдены вхождения подстроки в тексте на позициях:", occurrences)
else:
    print("Подстрока не найдена в тексте.")
