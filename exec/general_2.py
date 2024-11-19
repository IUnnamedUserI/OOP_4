#!/usr/bin/env python3
# -*- coding: utf-8 -*

'''
Написать программу, которая будет генерировать матрицу из случайных целых
чисел. Пользователь может указать число строк и столбцов, а также диапазон
чисел. Произвести обработку ошибок ввода пользователя.
'''

import random


class MinValueBiggest(Exception):
    '''
    Пустое исключение, вызываемое в случае, если минимальное значение
    чисел для случайной генерации оказалось больше максимального
    '''
    pass


if __name__ == '__main__':
    '''
    Основное тело программы
    '''
    try:
        matrix_width = int(input("Введите ширину матрицы: "))
        matrix_height = int(input("Введите высоту матрицы: "))
        min_value = int(input("Введите минимальное значение диапазона: "))
        max_value = int(input("Введите максимальное значение диапазона: "))

        if min_value > max_value:
            raise MinValueBiggest  # Вызов исключения

        matrix = [[0] * matrix_width for _ in range(matrix_height)]

        for i in range(matrix_height):  # Заполнение матрицы
            for j in range(matrix_width):
                matrix[i][j] = random.randint(min_value, max_value)

        for i in range(matrix_height):  # Вывод матрицы
            temp_str = str()
            j = 0
            for j in range(matrix_width):
                if j < matrix_width - 1:  # Проверка на последнее значение
                    temp_str += str(matrix[i][j]) + " "
                else:
                    temp_str += str(matrix[i][j])
                j += 1
            print(f"|{temp_str}|")
        print('Завершение работы')

    except ValueError:  # Ошибка при неправильном указании чисел
        print('Ошибка: Ошибка при вводе чисел')
    except MinValueBiggest:  # Ошибка при указании min больше max
        print("Ошибка: Минимальное значение больше максимального")
