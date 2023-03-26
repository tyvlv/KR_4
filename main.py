import json
import os

from classes import HH, SuperJob, Vacancy, Engine


def main():
    file_path = os.path.join('vacancy_list.json')
    connector = Engine.get_connector(file_path)

    hh = HH()
    vacancy_list1 = hh.get_request("Python")
    # print(json.dumps(vacancy_list1, indent=2, ensure_ascii=False))
    # print(len(vacancy_list1))

    sb = SuperJob()
    vacancy_list2 = sb.get_request("Python")
    # print(json.dumps(vacancy_list2, indent=2, ensure_ascii=False))
    # print(len(vacancy_list2))
    # print(Vacancy(vacancy_list2[99]).__repr__())
    # print(Vacancy(vacancy_list2[99]))

    connector.insert(vacancy_list1)
    print(connector.select({'salary': {"from": 80000, "to": 120000}}))
    print(connector.delete({'salary': {'from': 0, 'to': 60000}}))
    print(connector.select({'salary': {'from': 0, 'to': 60000}}))

if __name__ == "__main__":
    main()
