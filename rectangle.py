"""
    ---Task 1 ---
    Задание №6
 * Изменяем класс прямоугольника.
 * Заменяем пару декораторов проверяющих длину и ширину на дескриптор с валидацией размера.
"""
class Validator:
    def __init__(self, name, min_value, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"{self.name.capitalize()} должен быть между {self.min_value} и {self.max_value}")
        setattr(instance, self.name, value)
class Rectangle:
    __slots__ = ('_height', '_width')

    def __init__(self, height: int, width=None):
        self._height = height
        if width:
            self._width = width
        else:
            self._width = height

    def get_perimetr(self):
        return 2 * (self._height + self._width)

    def get_area(self):
        return self._width * self._height

    height = Validator('_height', 1, 100)
    width = Validator('_width', 1, 100)

    def __str__(self):
        return f'Прямоугольник({self._height}x{self._width}), S= {self.get_area()}'

    def __repr__(self):
        return f'размеры:({self._height}x{self._width}), S= {self.get_area()}'


if __name__ == "__main__":
    rect = Rectangle(2, 5)
    try:
        rect.width = 200
        print(rect)
    except ValueError as e:
        print('Error:', e)