"""
Модуль для оценки площади треугольника методом Монте-Карло.

Модуль содержит функции для многократного вычисления площади треугольника,
ограниченного прямоугольником, с использованием метода статистических
испытаний (Монте-Карло), а также для расчета математического ожидания
и дисперсии полученных оценок.
"""

import random
import math
import sys
import numpy as np


def triangle(a: float, b: float, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, N: int) -> float:
    """
    Оценивает площадь треугольника методом Монте-Карло за один эксперимент.

    Аргументы:
        a (float): Длина прямоугольника по оси X
        b (float): Длина прямоугольника по оси Y
        x1, y1, x2, y2, x3, y3 (float): Координаты вершин треугольника
        N (int): Количество случайных точек в эксперименте

    Возвращает:
        float: Оценка площади треугольника
    """
    N0 = 0  # счетчик точек внутри треугольника
    
    for i in range(N):
        # Генерация случайной точки внутри прямоугольника
        x0 = random.uniform(0, a)
        y0 = random.uniform(0, b)

        # Векторы a b c
        Xa = np.array([x1 - x0, y1 - y0])
        Xb = np.array([x2 - x0, y2 - y0])
        Xc = np.array([x3 - x0, y3 - y0])

        # Длины векторов
        len_a = np.linalg.norm(Xa)
        len_b = np.linalg.norm(Xb)
        len_c = np.linalg.norm(Xc)
        
        if len_a == 0 or len_b == 0 or len_c == 0:
            N0 += 1
            continue

        # Углы между векторами a b c
        angle1 = math.acos(np.dot(Xa, Xb) / (len_a * len_b))
        angle2 = math.acos(np.dot(Xb, Xc) / (len_b * len_c))
        angle3 = math.acos(np.dot(Xc, Xa) / (len_c * len_a))

        sum_angle = angle1 + angle2 + angle3

        if abs(sum_angle - 2 * math.pi) < 1e-10:
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
    - R: радиус треугольника
    - X0, Y0: координаты центра треугольника
    - N: количество точек в одном эксперименте

    По результатам экспериментов рассчитывает:
    - Математическое ожидание оценок
    - Дисперсию оценок
    - Истинную площадь треугольника для сравнения

    Выводит результаты на экран.
    """
    # Ввод параметров
    a = float(input("A = "))
    b = float(input("B = "))
    x1 = float(input("x1 = "))
    y1 = float(input("y1 = "))
    x2 = float(input("x2 = "))
    y2 = float(input("y2 = "))
    x3 = float(input("x3 = "))
    y3 = float(input("y3 = "))
    N = int(input("N = "))

    vertices = [(x1, y1), (x2, y2), (x3, y3)]
    for i, (x, y) in enumerate(vertices, 1):
        if x < 0 or x > a or y < 0 or y > b:
            sys.exit("Треугольник не находится в прямоугольнике полностью")
    
    # Проведение серии экспериментов
    areas = []
    iterations = 10
    for i in range(iterations):
        S = triangle(a, b, x1, y1, x2, y2, x3, y3, N)
        areas.append(S)
    
    # Расчет статистических характеристик
    ozhid = ozhidanie(areas)
    disp = dispertion(areas, ozhid)
    
    # Вывод результатов
    print(f"\nОценки: {[round(s, 4) for s in areas]}")
    print(f"Матожидание: {ozhid:.7f}")
    print(f"Дисперсия: {disp:.8f}")
    print(f"Истинная площадь πR² = {abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2:.6f}")


if __name__ == "__main__":
    main()