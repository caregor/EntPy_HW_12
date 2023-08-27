"""
    ---Task 2---
    Создайте класс студента.
* Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
* Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
* Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
* Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых.
"""
import csv
import random


class Validator:
    def __init__(self, name, valid_type, is_only_letter=False, name_istitle=False, min_value=None, max_value=None):
        self.name = name
        self.valid_is_only_letter = is_only_letter
        self.name_istitle = name_istitle
        self.valid_type = valid_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.valid_type):
            raise ValueError(f"{self.name} must be of type {self.valid_type.__name__}.")

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be greater than or equal to {self.min_value}.")

        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be less than or equal to {self.max_value}.")

        if self.valid_is_only_letter  and not value.isalpha():
            raise ValueError(f"{self.name} must contain only letters.")

        if self.name_istitle  and not value.istitle():
            raise ValueError(f"{self.name} must start with a capital letter.")

        instance.__dict__[self.name] = value


class Subject:
    def __init__(self, name):
        self.name = name
        self._grade = None
        self.test_results = {}

    def add_test_result(self, test_name, result):
        test_result_validator = Validator('test_result', int, min_value=0, max_value=100)
        test_result_validator.__set__(self, result)
        self.test_results[test_name] = result

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        grade_validator = Validator('grade', int, min_value=2, max_value=5)
        grade_validator.__set__(self, value)
        self._grade = value

    def average_test_score(self):
        if len(self.test_results) == 0:
            return 0

        total_score = sum(self.test_results.values())
        return total_score / len(self.test_results)


class Student:
    first_name = Validator('first_name', str, is_only_letter=True, name_istitle=True)
    last_name = Validator('last_name', str, is_only_letter=True, name_istitle=True)

    def __init__(self, first_name, last_name, subjects_file):
        self.first_name = first_name
        self.last_name = last_name
        self.subjects = self.load_subjects(subjects_file)

    def load_subjects(self, subjects_file):
        subjects = []
        with open(subjects_file, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                subjects.append(Subject(row[0]))
        return subjects

    def overall_average_grade(self):
        total_subjects = len(self.subjects)
        total_grades = sum(subject.grade for subject in self.subjects)
        return total_grades / total_subjects if total_subjects > 0 else 0


if __name__ == "__main__":
    try:
        student = Student("Ivan", "Ivanov", "subjects.csv")
        print("Student created:", student.first_name, student.last_name)

        for subject in student.subjects:
            print("Subject:", subject.name)

            try:
                subject.grade = random.randint(2,5)
                print("Grade:", subject.grade)
            except ValueError as e:
                print("Error:", e)

            try:
                subject.add_test_result("Test 1", 85)
                print("Test result:", subject.test_results["Test 1"])

                subject.add_test_result("Test 2", 90)
                print("Test result:", subject.test_results["Test 2"])
            except ValueError as e:
                print("Error:", e)

            print("Average test score:", subject.average_test_score())
            print()
        print("Overall average grade:", student.overall_average_grade())

    except ValueError as e:
        print("Error:", e)
    except FileNotFoundError:
        print("Subjects file not found.")