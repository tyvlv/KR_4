import json
import os
from abc import ABC, abstractmethod

import requests


class Connector:
    """Класс коннектор к файлу"""
    __data_file = None

    def __init__(self, file_path: str):
        self.__data_file = file_path
        self.__connect()

    @property
    def data_file(self) -> str:
        return self.__data_file

    @data_file.setter
    def data_file(self, file_path: str):
        """Установка файла по указанному пути"""
        self.__data_file = file_path
        self.__connect()

    def __connect(self):
        """Перезаписывает или создает новый пустой файл"""
        with open(self.__data_file, 'w') as file:
            json.dump([], file)

    def insert(self, data: list):
        """Запись данных в файл"""
        with open(self.__data_file, 'w', encoding='UTF-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def select(self, query: dict) -> list:
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        result = []
        with open(self.__data_file, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        if not query:
            return data

        for item in data:
            if all(item.get(key) == value for key, value in query.items()):
                result.append(item)

        return result

    def delete(self, query: dict):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not query:
            return

        result = []
        with open(self.__data_file, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        for item in data:
            if not all(item.get(key) == value for key, value in query.items()):
                result.append(item)

        with open(self.__data_file, 'w', encoding='UTF-8') as file:
            json.dump(result, file, indent=2, ensure_ascii=False)


class Engine(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_request(self, search: str):
        pass

    @staticmethod
    def get_connector(file_name: str) -> Connector:
        """ Возвращает экземпляр класса Connector """
        return Connector(file_name)


class HH(Engine):
    URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.vacancy_list = []

    def get_request(self, search: str) -> list:
        """Получает информацию через API"""
        for page in range(1):
            params = {
                'text': f'NAME:{search}',  # Текст фильтра
                'area': 113,  # Поиск осуществляется по вакансиям в России
                'page': page,  # Индекс страницы поиска на HH
                'per_page': 100  # Кол-во вакансий на 1 странице
            }
            req = requests.get(self.URL, params).json()['items']
            for item in req:
                if item.get('salary') is not None and item.get('salary').get('currency') is not None:
                    # если зарплата в рублях, добавляем данные в список вакансий
                    if item.get('salary').get('currency') == "RUR":
                        self.vacancy_list.append(self.get_info_vacancy(item))
                    else:
                        continue
                    # если зарплата не указана, добавляем данные в список вакансий
                else:
                    self.vacancy_list.append(self.get_info_vacancy(item))
        return self.vacancy_list

    @staticmethod
    def get_info_vacancy(vacancy: dict) -> dict:
        """Выбирает нужную информацию о вакансии"""
        info_vacancy = {
            'name': vacancy['name'],
            'url': vacancy['alternate_url'],
            'description': vacancy['snippet']['responsibility'],
            'salary': {'from': 0 if vacancy.get('salary') is None else vacancy.get('salary', {}).get('from', 0),
                       'to': 0 if vacancy.get('salary') is None else vacancy.get('salary', {}).get('to', 0), }
        }
        return info_vacancy


class SuperJob(Engine):
    URL = "https://api.superjob.ru/2.0/vacancies/"
    HEADERS = {"X-Api-App-Id": os.getenv('SuperjobAPI_key')}

    def __init__(self):
        self.vacancy_list = []

    def get_request(self, search: str):
        for page in range(1):
            params = {
                'keyword': f'{search}',  # Текст фильтра
                'page': page,  # Индекс страницы поиска на HH
                'count': 100  # Кол-во вакансий на 1 странице
            }
            req = requests.get(self.URL, headers=self.HEADERS, params=params).json()['objects']
            for item in req:
                self.vacancy_list.append(self.get_info_vacancy(item))
        return self.vacancy_list

    @staticmethod
    def get_info_vacancy(vacancy: dict) -> dict:
        """Выбирает нужную информацию о вакансии"""
        info_vacancy = {
            'name': vacancy['profession'],
            'url': vacancy['link'],
            'description': vacancy['candidat'],
            'salary': {'from': vacancy['payment_from'],
                       'to': vacancy['payment_to'], }
        }
        return info_vacancy


class Vacancy:
    __slots__ = ('name', 'url', 'description', 'salary')

    def __init__(self, vacancy: dict):

        self.name = vacancy['name']
        self.url = vacancy['url']
        self.description = vacancy['description'].replace('\n', '')
        self.salary = vacancy['salary']

    def __str__(self):
        return f'Вакансия - {self.name}, заработная плата - {self.get_salary()}'

    def __repr__(self):
        return f'"name": {self.name}\n \
               "url": {self.url}\n \
               "description": {self.description}\n \
               "salary": {self.salary}'

    def get_salary(self) -> str:
        """Возвращает зарплату в строковом представлении"""

        if self.salary is not None:

            if self.salary['from'] != 0 and self.salary['to'] != 0:
                return f"от {self.salary['from']} до {self.salary['to']} руб/мес"

            elif self.salary['from'] == 0 and self.salary['to'] != 0:
                return f"до {self.salary['to']} руб/мес"

            elif self.salary['from'] != 0 and self.salary['to'] == 0:
                return f"от {self.salary['from']} руб/мес"

            elif self.salary['from'] == 0 and self.salary['to'] == 0:
                return 'не указана'

        return 'не указана'


class HHVacancy(Vacancy):
    """ HeadHunter Vacancy """

    def __str__(self):
        return f'HH: {self.name}, зарплата: {self.get_salary()}'


class SJVacancy(Vacancy):
    """ SuperJob Vacancy """

    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.get_salary()}'


