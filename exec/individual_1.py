#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Выполнить индивидуальное задание 1 лабораторной работы 2.19,
добавив возможность работы с исключениями и логгирование.
'''

import json
from datetime import datetime
import argparse
import pathlib
import logging


class DateError(Exception):
    pass


def print_help():
    """
    Функция вывода доступных пользователю команд.

    Аргументы:
        None

    Возвращает:
        None
    """

    print("list - вывод всех добавленных записей")
    print("add - добавление новых записей")
    print("find - найти запись по фамилии")
    print("exit - завершение работы программы")


def add_worker(workers, surname, name, phone, date):
    """
    Функция добавления новой записи в список.

    Аргументы:
        workers (list) - Список, в который будет добавляться запись
        surname (str) - Фамилия добавляемого сотрудника
        name (str) - Имя добавляемого сотрудника
        phone (int) - Номер телефона добавляемого сотрудника
        date (datetime) - Дата нанятия добавляемого сотрудника

    Возвращает:
        workers (list) - Обновлённый список сотрудников
    """

    try:
        phone = int(phone)
        if not isinstance(phone, int):  # Проверка номера на правильность
            raise ValueError

        temp_data = str(date).split('.')
        for i in range(len(temp_data)):
            temp_data[i] = int(temp_data[i])
            if not isinstance(temp_data[i], int):
                raise DateError

        if (temp_data[0] < 0 or temp_data[0] > 31):
            raise DateError
        if (temp_data[1] < 0 or temp_data[1] > 12):
            raise DateError
        if (temp_data[2] < 1900 or temp_data[2] > 2024):
            raise DateError

        workers.append(
            {
                "surname": surname,
                'name': name,
                'phone': phone,
                'date': date
            }
        )
        logging.info(
            f"Добавлен сотрудник: {surname} {name}, "
            f"поступивший {date}. Номер телефона: {phone}"
        )

    except ValueError:
        print("Ошибка при указании номера")
        logging.error("Не удалось добавить запись:"
                      "ошибка при указании номера телефона")
    except DateError:
        print("Ошибка при указании даты")
        logging.error("Не удалось добавить запись: ошибка при указании даты")

    return workers


def print_list(list):
    """
    Функция выводит на экран список всех существующих записей.

    Аргументы:
        list (list) - Список всех сотрудников (записей) для вывода

    Возвращает:
        None
    """
    count = 0

    for member in list:
        print(f"{member['surname']} {member['name']} | "
              f"{member['phone']} | {member['date']}")
        count += 1

    logging.info(f"Выведен список сотрудников. Всего: {count}")


def find_member(workers, period):
    """
    Функция для вывода на экран всех записей, чей стаж работы больше
    или равен указанному.

    Аргументы:
        workers (list) - Список сотрудников для поиска
        period (int) - Количество лет стажа

    Возвращает:
        members (list) - Сипсок сотрудников, чей стаж больше
            или равен указанному
    """

    count = 0
    members = []

    for member in workers:
        year = datetime.strptime(member['date'], "%d.%m.%Y").year
        if datetime.now().year - period >= year:
            members.append(member)
            count += 1

    logging.info(f"Проведена выборка (период - {period}). "
                 f"Результат: {count} записей.")

    if count == 0:
        print("Записи не найдены")
    else:
        return members


def get_home_path(filename):
    """
    Получение полного пути к файлу, расположенному в домашнем каталоге
    пользователя (пример: C:/Users/<имя_пользователя>/<имя_файла>).

    Аргументы:
        filename (str) - Имя файла

    Возвращает:
        Полный путь к файлу (str)
    """
    home_dir = pathlib.Path.home()
    return home_dir / filename


def save_file(filename, workers):
    """
    Сохранение списка сотрудников в файл.

    Аргументы:
        filename (str) - Имя сохраняемого файла
        workers (list) - Список сохраняемых сотрудников (записей)

    Возвращает:
        None
    """
    try:
        with open(get_home_path(filename), "w", encoding="utf-8") as file:
            file_path = get_home_path(filename)
            logging.info(f"Сохранение файла по пути: {file_path}")
            json.dump(workers, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Ошибка при сохранении файла: {e}")


def load_file(filename):
    """
    Загрузка данных о сотрудниках из указанного JSON-файла.

    Аргументы:
        filename (str) - Имя загружаемого файла

    Возвращает:
        file (list) - список записей из файла
        Пустой список - если произошла ошибка с при чтении файла
    """
    try:
        with open(get_home_path(filename), "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка загрузки JSON: {e}")
        print("Файл поврежден или имеет некорректный формат.")
        return []
    except FileNotFoundError:
        logging.warning("Файл не найден. Создан пустой список.")
        return []


def parse_datetime(value):
    """
    Преобразование указанного значения в формат даты.

    Аргументы:
        value (str) - указанная дата в текстовом формате

    Возвращает:
        Дата (datetime) - Преобразованное значение value в формат datetime
        Текст 'Error' - В случае ошибки преобразования
    """
    try:
        return datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        print("Error")


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-s",
        "--surname",
        action="store",
        required=True,
        help="The worker's surname"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The worker's name"
    )
    add.add_argument(
        "-p",
        "--phone",
        action="store",
        help="The worker's phone"
    )
    add.add_argument(
        "-d",
        "--date",
        action="store",
        required=True,
        help="The date of hiring"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-p",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    try:
        workers = load_file(args.filename)
    except FileExistsError:
        workers = []

    if args.command == "add":
        workers = add_worker(
            workers,
            args.surname,
            args.name,
            args.phone,
            args.date
        )
        is_dirty = True

    elif args.command == "display":
        print_list(workers)

    elif args.command == "select":
        selected = find_member(workers, args.period)
        print_list(selected)

    if is_dirty:
        save_file(args.filename, workers)


if __name__ == "__main__":
    """
    Основная программа
    """

    logging.basicConfig(
        filename='individual_1.log',
        level=logging.INFO
    )

    main()
