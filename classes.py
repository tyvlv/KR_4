import json
import os
from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_request(self, search: str):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


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
