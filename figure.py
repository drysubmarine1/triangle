"""
Модуль для оценки площади многоугольника методом Монте-Карло.

Модуль содержит функции для многократного вычисления площади многоугольника,
ограниченного прямоугольником, с использованием метода статистических
испытаний (Монте-Карло), а также для расчета математического ожидания
и дисперсии полученных оценок.
"""

import random
import sys


def figure(a: float, b: float, vertices: list, N: int) -> float:
    """
    Оценивает площадь многоугольника методом Монте-Карло за один эксперимент.

    Аргументы:
        a (float): Длина прямоугольника по оси X
        b (float): Длина прямоугольника по оси Y
        vertices (list): Список вершин многоугольника
        N (int): Количество случайных точек в эксперименте

    Возвращает:
        float: Оценка площади многоугольника
    """
    N0 = 0  # счетчик точек внутри треугольника
    n = len(vertices)
    for i in range(N):
        # Генерация случайной точки внутри прямоугольника
        x = random.uniform(0, a)
        y = random.uniform(0, b)

        inside = False
        for j in range(n):
            x1, y1 = vertices[j]
            x2, y2 = vertices[(j+1) % n]
            # Проверяем, пересекает ли горизонтальная линия из точки ребро
            if (y1 > y) != (y2 > y):
            # Находим x координату пересечения
                x_intersect = x2 - (y2 - y) * (x2 - x1) / (y2 - y1)
            # Если точка левее пересечения
                if x_intersect > x:
                    inside = not inside
        if inside == True:
            N0 += 1
        
    # Оценка площади треугольника: (доля точек) * (площадь прямоугольника)
    S = N0 / N * a * b
    return S


def ozhidanie(areas: list) -> float:
    """
    Вычисляет математическое ожидание (среднее арифметическое) оценок площади.

    Аргументы:
        areas (list): Список оценок площади из нескольких экспериментов

    Возвращает:
        float: Среднее арифметическое значений в списке
    """
    return sum(areas) / len(areas)


def dispertion(areas: list, ozhid: float) -> float:
    """
    Вычисляет несмещенную оценку дисперсии для полученных оценок площади.

    Аргументы:
        areas (list): Список оценок площади из нескольких экспериментов
        ozhid (float): Математическое ожидание (среднее значение)

    Возвращает:
        float: Несмещенная оценка дисперсии
    """
    disp_sum = 0
    for i in areas:
        disp_sum += (i - ozhid) ** 2
    
    return disp_sum / (len(areas) - 1)


def main():
    """
    Основная функция программы.

    Запрашивает у пользователя параметры задачи:
    - A, B: стороны прямоугольника
    - Координаты вершин многоугольника
    - N: количество точек в одном эксперименте

    По результатам экспериментов рассчитывает:
    - Математическое ожидание оценок
    - Дисперсию оценок
    - Истинную площадь для сравнения

    Выводит результаты на экран.
    """
    # Ввод параметров
    a = float(input("A = "))
    b = float(input("B = "))
    N_vershin = int(input("N_vershin = "))
    
    vertices = []
    print("\nВведите координаты вершин (x y):")
    for i in range(N_vershin):
        x, y = map(float, input(f"Вершина {i+1}: ").split())
        vertices.append((x, y))

    N = int(input("N = "))
    
    for i, (x, y) in enumerate(vertices, 1):
        if x < 0 or x > a or y < 0 or y > b:
            sys.exit("Треугольник не находится в прямоугольнике полностью")
    
    # Проведение серии экспериментов
    areas = []
    iterations = 10
    for i in range(iterations):
        S = figure(a, b, vertices, N)
        areas.append(S)
    
    # Расчет статистических характеристик
    ozhid = ozhidanie(areas)
    disp = dispertion(areas, ozhid)

    n = len(vertices)
    area = 0
    # Расчёт истинной плоащид фигуры
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    
    # Вывод результатов
    print(f"\nОценки: {[round(s, 4) for s in areas]}")
    print(f"Матожидание: {ozhid:.7f}")
    print(f"Дисперсия: {disp:.8f}")
    print(f"Истинная площадь = {abs(area / 2):.6f}")


if __name__ == "__main__":
    main()