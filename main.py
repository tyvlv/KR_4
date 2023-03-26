import json
import os

from classes import HH, SuperJob, Vacancy, Engine
from utils import get_vacancies, sorting_by_salary, get_top_by_salary


def main():
    file_path = os.path.join('vacancy_list.json')
    connector = Engine.get_connector(file_path)

    while True:
        print("Где будем искать вакансии:\n1 - HeadHunter\n2 - SuperJob")
        hh_sj_site = input()
        if hh_sj_site in ['1', '2']:
            break
        else:
            print("Введите '1' или '2'")

    print("Введите ключевое слово, по которому будем искать вакансии:")
    search = input()

    while True:
        print("Искать вакансии без опыта работы:\n1 - Да\n2 - Не важно")
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
        print(f"Найдено {len(vacancy_list)} вакансий")
        connector.insert(vacancy_list)
    else:
        print("Вакансии с таким ключевым словом не существует. Программа завершена")
        quit()

    # hh = HH()
    # vacancy_list1 = hh.get_request("Python", "noExperience")
    # # print(json.dumps(vacancy_list1, indent=2, ensure_ascii=False))
    # # print(len(vacancy_list1))
    #
    # sb = SuperJob()
    # vacancy_list2 = sb.get_request("Python", "noExperience")
    # # print(json.dumps(vacancy_list2, indent=2, ensure_ascii=False))
    # # print(len(vacancy_list2))
    # # print(Vacancy(vacancy_list2[99]).__repr__())
    # # print(Vacancy(vacancy_list2[99]))
    #
    # connector.insert(vacancy_list1)
    # # print(connector.select({'salary': {"from": 80000, "to": 120000}}))
    # # print(connector.delete({'salary': {'from': 0, 'to': 60000}}))
    # # print(connector.select({'salary': {'from': 0, 'to': 60000}}))
    #
    # hh_sj_vacancy_list = get_vacancies(vacancy_list1, 1)
    # hh_sj_vacancy_list_sort = sorting_by_salary(hh_sj_vacancy_list)
    # print(get_top_by_salary(hh_sj_vacancy_list_sort, 10))


if __name__ == "__main__":
    main()
