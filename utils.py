from classes import HHVacancy, SJVacancy


def get_vacancies(vacancy_list: list, hh_sj_site: str) -> list[HHVacancy] | list[SJVacancy]:
    """Возвращает экземпляры HHVacancy/SJVacancy"""
    hh_vacancy_list = []
    sj_vacancy_list = []
    if hh_sj_site == '1':
        for vacancy in vacancy_list:
            hh_vacancy_list.append(HHVacancy(vacancy))
        return hh_vacancy_list

    for vacancy in vacancy_list:
        sj_vacancy_list.append(SJVacancy(vacancy))
    return sj_vacancy_list


def sorting_by_salary(hh_sj_vacancy_list: list) -> list:
    """Сортирует список вакансий по убыванию зарплаты (поле "от")"""
    return sorted(hh_sj_vacancy_list, key=lambda k: k.salary['from'], reverse=True)


def get_top_by_salary(hh_sj_vacancy_list: list, top_count: int) -> list:
    """Возвращает top_count вакансий с максимальной зарплатой"""
    top_vacancies = hh_sj_vacancy_list[:top_count]
    return top_vacancies
