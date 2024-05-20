import os
import random
import unittest

# хранит полное имя студента 
class Student:
    def __init__(self, full_name):
        self.full_name = full_name

    def __str__(self):
        return self.full_name

# хранит название темы и список вопросов 
class Topic:
    def __init__(self, name):
        self.name = name
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def get_random_question(self):
        if not self.questions:
            raise ValueError(f"Нет больше доступных вопросов в теме: {self.name}")
        return self.questions.pop(random.randint(0, len(self.questions) - 1))

# загружает студентов и темы из файлов, генерирует билеты для студентов на основе заданной структуры 
class ExamTicketGenerator:
    def __init__(self, students_file, topics_file):
        self.students = self._load_students(students_file)
        self.topics = self._load_topics(topics_file)

    def _load_students(self, students_file):
        with open(students_file, 'r', encoding='utf-8') as file:
            return [Student(line.strip()) for line in file.readlines()]

    def _load_topics(self, topics_file):
        topics = {}
        current_topic = None
        with open(topics_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith("Тема:"):
                    current_topic = Topic(line.replace("Тема:", "").strip())
                    topics[current_topic.name] = current_topic
                elif current_topic:
                    current_topic.add_question(line)
        return topics

    def generate_tickets(self, structure, output_file):
        with open(output_file, 'w', encoding='utf-8') as file:
            for student in self.students:
                file.write(f"{student}\n")
                tickets = []
                for topic_name, count in structure.items():
                    topic = self.topics[topic_name]
                    questions = []
                    for _ in range(count):
                        questions.append(topic.get_random_question())
                    tickets.append(f"({topic_name}: {', '.join(questions)})")
                file.write(f"{' '.join(tickets)}\n\n")

# считывает пути к файлам и структуру билета из консоли, создаёт экземпляр ExamTicketGenerator и генерирует билеты 
def main():
    students_file = input("Введите путь к файлу со студентами: ")
    topics_file = input("Введите путь к файлу с темами и вопросами: ")
    output_file = input("Введите путь к выходному файлу: ")

    structure = {}
    print("Введите структуру билета (Тема: количество вопросов), по окончании введите 'end':")
    while True:
        entry = input()
        if entry == 'end':
            break
        topic, count = entry.split(':')
        structure[topic.strip()] = int(count.strip())

    generator = ExamTicketGenerator(students_file, topics_file)
    generator.generate_tickets(structure, output_file)
    print(f"Билеты сгенерированы и сохранены в файл {output_file}")

# содержит тесты для проверки загрузки студентов и тем
class TestExamTicketGenerator(unittest.TestCase):
    def setUp(self):
        self.students_file = 'students.txt'
        self.topics_file = 'topics.txt'
        with open(self.students_file, 'w', encoding='utf-8') as file:
            file.write("Иванов Иван Иванович\nПетров Петр Петрович\n")
        with open(self.topics_file, 'w', encoding='utf-8') as file:
            file.write("Тема: Алгоритмы\nАлгоритм Дейкстры\nАлгоритм обхода графа\n")
            file.write("Тема: Задачи\nНайти максимальное из 3-х чисел\nВыяснить является ли введенная строка палиндромом\n")

    def tearDown(self):
        os.remove(self.students_file)
        os.remove(self.topics_file)

    def test_load_students(self):
        generator = ExamTicketGenerator(self.students_file, self.topics_file)
        self.assertEqual(len(generator.students), 2)
        self.assertEqual(generator.students[0].full_name, "Иванов Иван Иванович")

    def test_load_topics(self):
        generator = ExamTicketGenerator(self.students_file, self.topics_file)
        self.assertEqual(len(generator.topics), 2)
        self.assertIn("Алгоритмы", generator.topics)
        self.assertEqual(len(generator.topics["Алгоритмы"].questions), 2)

if __name__ == "__main__":
    main()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
