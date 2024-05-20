# строит таблицу переходов для конечного автомата 
def build_transition_table(pois):
    alphabet_size = 256
    A = len(pois)
    TF = [[0] * alphabet_size for _ in range(A + 1)]

    for state in range(A + 1):
        for x in range(alphabet_size):
            TF[state][x] = next_state(pois, A, state, x)
    return TF

# вычисляет следующее состояние автомата 
def next_state(pois, A, state, x):
    if state < A and x == ord(pois[state]):
        return state + 1

    i = 0
    for k in range(state, 0, -1):
        if ord(pois[k - 1]) == x:
            while i < k - 1:
                if pois[i] != pois[state - k + 1 + i]:
                    break
                i += 1
            if i == k - 1:
                return k
    return 0

# ищет вхождения подстроки в тексте, используя конечный автомат 
def finite_automaton_matcher(text, pattern):
    alphabet_size = 256
    A = len(pattern)
    TF = build_transition_table(pattern)

    state = 0
    for i in range(len(text)):
        state = TF[state][ord(text[i])]
        if state == A:
            print("Найдено вхождение подстроки на позиции", i - A + 1)

# пример
text = "Hello, how are you today?"
pattern = "are"
finite_automaton_matcher(text, pattern)






