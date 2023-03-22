import json
import os
from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_request(self, vacancy_name: str):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"
        self.vacancy_list = []

    def get_request(self, vacancy_name: str):
        for item in range(2):
            params = {
                'text': f'NAME:{vacancy_name}',  # Текст фильтра
                'area': 113,  # Поиск осуществляется по вакансиям в России
                'page': item,  # Индекс страницы поиска на HH
                'per_page': 100  # Кол-во вакансий на 1 странице
            }
            req = requests.get(self.url, params).json()['items']
            for i in req:
                self.vacancy_list.append(i)
        return self.vacancy_list


class SuperJob(Engine):
    def __init__(self):
        self.url = "https://api.superjob.ru/2.0/vacancies/"
        self.vacancy_list = []

    def get_request(self, vacancy_name: str):
        headers = {"X-Api-App-Id": os.getenv('SuperjobAPI_key')}
        for item in range(2):
            params = {
                'keyword': f'{vacancy_name}',  # Текст фильтра
                'page': item,  # Индекс страницы поиска на HH
                'count': 100  # Кол-во вакансий на 1 странице
            }
            req = requests.get(self.url, headers=headers, params=params).json()['objects']
            for i in req:
                self.vacancy_list.append(i)
        return self.vacancy_list


hh = HH()
vacancy_list1 = hh.get_request("Python")
print(json.dumps(vacancy_list1, indent=2, ensure_ascii=False))
print(len(vacancy_list1))

# sb = SuperJob()
# vacancy_list2 = sb.get_request("Python")
# print(json.dumps(vacancy_list2, indent=2, ensure_ascii=False))
# print(len(vacancy_list2))
