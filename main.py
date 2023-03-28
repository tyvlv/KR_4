import os
import sys

from classes import HH, SuperJob, Engine
from utils import get_vacancies, sorting_by_salary, get_top_by_salary


def main():
    file_path = os.path.join('vacancy_list.json')
    connector = Engine.get_connector(file_path)

    while True:
        print("Где будем искать вакансии?\n1 - HeadHunter\n2 - SuperJob")
        hh_sj_site = input()
        if hh_sj_site in ['1', '2']:
            break
        else:
            print("Введите '1' или '2'")

    print("Введите ключевое слово, по которому будем искать вакансии:")
    search = input()

    while True:
        print("Искать вакансии без опыта работы?\n1 - Да\n2 - Не важно")
        experience = input()
        if experience == '1':
            if hh_sj_site == '1':
                hh = HH()
                vacancy_list = hh.get_request(search, "noExperience")
                break
            elif hh_sj_site == '2':
                sb = SuperJob()
                vacancy_list = sb.get_request(search, "noExperience")
                break
        elif experience == '2':
            if hh_sj_site == '1':
                hh = HH()
                vacancy_list = hh.get_request(search)
                break
            elif hh_sj_site == '2':
                sb = SuperJob()
                vacancy_list = sb.get_request(search)
                break
        else:
            print("Введите '1' или '2'")

    if vacancy_list:
        print(f"Найдено {len(vacancy_list)} вакансий, которые помещены в файл {file_path}.")
        connector.insert(vacancy_list)
    else:
        print("Вакансии с таким ключевым словом не существует. Программа завершена.")
        sys.exit()

    while True:
        print("Хотите поработать с полученными данными?\n1 - Да\n2 - Нет")
        user_choice = input()
        if user_choice == '1':
            vacancy_list_from_file = connector.select({})
            hh_sj_vacancy_list = get_vacancies(vacancy_list_from_file, hh_sj_site)
            break
        elif user_choice == '2':
            print("Программа завершена.")
            sys.exit()
        else:
            print("Введите '1' или '2'")

    while True:
        print(f"Что будем делать?\n\
1 - Вывести в консоль N вакансий по запросу '{search}'\n\
2 - Вывести в консоль N вакансий по убыванию зарплаты")
        user_choice_action = input()

        if user_choice_action == '1':
            try:
                number_of_vacancies = int(input("Введите количество вакансий N:\n"))
                print(hh_sj_vacancy_list[:number_of_vacancies])
                break
            except ValueError:
                print("Вы ввели не число. Давайте еще раз попробуем...")
                continue

        elif user_choice_action == '2':
            try:
                number_of_vacancies = int(input("Введите количество вакансий N:\n"))
                print(get_top_by_salary(sorting_by_salary(hh_sj_vacancy_list), number_of_vacancies))
                break
            except ValueError:
                print("Вы ввели не число. Давайте еще раз попробуем...")
                continue

        print("Введите '1' или '2'")


if __name__ == "__main__":
    main()
