import unittest
import random
import math
from figure import figure, ozhidanie, dispertion

class TestCircleSimple(unittest.TestCase):
    
    def setUp(self):
        random.seed(42)  # для повторяемости

    def test_figure_basic(self):
        """Тест функции figure : фигура целиком внутри прямоугольника"""
        a, b, = 5, 5
        vertices = [(0, 0), (1, 0), (0, 1)]
        N = 10000
        
        # Запускаем несколько раз и проверяем
        results = []
        for i in range(10):
            S = figure(a, b, vertices, N)
            results.append(S)
        
        # Среднее должно быть близко к 0,5
        mean_result = sum(results) / len(results)
        self.assertAlmostEqual(mean_result, 0.5, delta=0.2)

    def test_ozhidanie(self):
        """Тест функции математического ожидания"""
        areas = [1, 2, 3, 4, 5]
        expected = sum(areas) / len(areas)
        result = ozhidanie(areas)
        self.assertEqual(result, expected)
    
    def test_dispertion(self):
        """Тест функции дисперсии"""
        areas = [1, 2, 3, 4, 5]
        ozhid = ozhidanie(areas)  # = 3
        expected = 2.5
        result = dispertion(areas, ozhid)
        self.assertAlmostEqual(result, expected)


if __name__ == '__main__':
    unittest.main()