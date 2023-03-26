from classes import HHVacancy, SJVacancy


def get_vacancies(vacancy_list: list, hh_sj_site: int) -> list[HHVacancy | SJVacancy]:
    """Возвращает экземпляры HHVacancy/SJVacancy"""
    hh_sj_vacancy_list = []
    for vacancy in vacancy_list:
        if hh_sj_site == 1:
            hh_sj_vacancy_list.append(HHVacancy(vacancy))
        elif hh_sj_site == 2:
            hh_sj_vacancy_list.append(SJVacancy(vacancy))
    return hh_sj_vacancy_list


def sorting_by_salary(hh_sj_vacancy_list: list) -> list:
    """Сортирует список вакансий по убыванию зарплаты (поле "от")"""
    return sorted(hh_sj_vacancy_list, key=lambda k: k.salary['from'], reverse=True)


def get_top_by_salary(hh_sj_vacancy_list: list, top_count: int) -> list:
    """Возвращает top_count вакансий с максимальной зарплатой"""
    top_vacancies = hh_sj_vacancy_list[:top_count]
    return top_vacancies
