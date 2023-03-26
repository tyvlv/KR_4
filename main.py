import json

from classes import HH, SuperJob, Vacancy


def main():
    hh = HH()
    vacancy_list1 = hh.get_request("Python")
    print(json.dumps(vacancy_list1, indent=2, ensure_ascii=False))
    print(len(vacancy_list1))

    sb = SuperJob()
    vacancy_list2 = sb.get_request("Python")
    print(json.dumps(vacancy_list2, indent=2, ensure_ascii=False))
    print(len(vacancy_list2))
    print(Vacancy(vacancy_list2[99]).__repr__())
    print(Vacancy(vacancy_list2[99]))


if __name__ == "__main__":
    main()
