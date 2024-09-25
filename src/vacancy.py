from typing import Any


class Vacancy:
    """Класс для работы с вакансиями"""

    id: int
    name: str
    location: str
    salary_from: float
    salary_to: float
    salary_string: str
    published_at: str
    url: str
    name_employer: str
    experience: str
    requirement: str
    responsibility: str

    __slots__ = (
        "id",
        "name",
        "location",
        "salary_from",
        "salary_to",
        "salary_string",
        "published_at",
        "url",
        "name_employer",
        "experience",
        "requirement",
        "responsibility",
    )

    def __init__(self, vacancy: dict) -> None:
        """Метод инициализации объектов класса"""

        for vacancy_attribute in self.__slots__:
            if self.__check_attribute(vacancy_attribute, list(vacancy.keys())):
                setattr(self, vacancy_attribute, vacancy[vacancy_attribute])
            else:
                setattr(self, vacancy_attribute, None)

    def __str__(self) -> str:
        """Метод вывода краткой информации о вакансии"""

        return f"{self.name} - Зарплата: {self.salary_string} - Город: {self.location}- Ссылка на вакансию: {self.url}"

    def __eq__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для равенства =="""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() == other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __ne__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для неравенства !="""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() != other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __lt__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора меньше <"""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() < other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __le__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора меньше или равно <="""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() <= other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __gt__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора больше >"""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() > other.__get_salary_for_comparison()
        else:
            raise TypeError

    def __ge__(self, other: Any) -> Any:
        """Метод сравнения вакансий по зарплате - для оператора больше или равно >="""

        if isinstance(other, Vacancy):
            return self.__get_salary_for_comparison() >= other.__get_salary_for_comparison()
        else:
            raise TypeError

    def get_salary(self) -> str:
        """Метод возвращает значение зарплаты в формате: От ... до ... """

        return self.salary_string

    def __get_salary_for_comparison(self) -> Any:
        """Метод возвращает значение зарплаты для сравнения."""

        return self.salary_from

    @staticmethod
    def __check_attribute(attribute: Any, keys: list) -> Any:
        """Метод валидации аттрибутов при создании объекта класса"""

        return attribute in keys

    @staticmethod
    def __get_attribute_value_from_hh(attribute: str, vacancy: dict) -> Any:
        """Метод привязки аттрибутов в данных от hh"""

        match attribute:
            case "id":
                return vacancy["id"]

            case "name":
                return vacancy["name"]

            case "location":
                return vacancy["area"]["name"]

            case "salary_from":
                if not vacancy["salary"]:
                    return 0

                if not vacancy["salary"]["from"]:
                    return 0

                return vacancy["salary"]["from"]

            case "salary_to":
                if not vacancy["salary"]:
                    return 0

                if not vacancy["salary"]["to"]:
                    return 0

                return vacancy["salary"]["to"]

            case "salary_string":
                if not vacancy["salary"]:
                    return "Зарплата не указана"

                if not vacancy["salary"]["from"] and not vacancy["salary"]["to"]:
                    return "Зарплата не указана"

                if not vacancy["salary"]["from"]:
                    return f"До {vacancy["salary"]["to"]}"

                if not vacancy["salary"]["to"]:
                    return f"От {vacancy["salary"]["from"]}"

                return f"От {vacancy["salary"]["from"]} до {vacancy["salary"]["to"]}"

            case "published_at":
                return vacancy["published_at"]

            case "url":
                return vacancy["alternate_url"]

            case "name_employer":
                return vacancy["employer"]["name"]

            case "experience":
                return vacancy["experience"]["name"]

            case "requirement":
                return vacancy["snippet"]["requirement"]

            case "responsibility":
                return vacancy["snippet"]["responsibility"]

            case _:
                return None

    @classmethod
    def vacancies_from_hh_processing(cls, vacancies: list[dict]) -> list[dict]:
        """Метод приведение данных от hh к формату для дальнейшей обработки"""

        vacancies_processing = []
        for vacancy in vacancies:
            vacancy_processing = {}
            for key in cls.__slots__:
                vacancy_processing[key] = cls.__get_attribute_value_from_hh(key, vacancy)
            vacancies_processing.append(vacancy_processing)
        return vacancies_processing

    def to_dict(self) -> dict:
        """Метод возвращает вакансию в формате словаря"""

        result = {}
        for attr in self.__slots__:
            result[attr] = getattr(self, attr)
        return result

    @staticmethod
    def get_list_of_vacancies(vacancies: list[dict]) -> list:
        """Метод создания списка объектов класса"""

        return [Vacancy(vacancy) for vacancy in vacancies]

    @staticmethod
    def get_list_of_dicts_vacancies(vacancies: list) -> list:
        """Метод создания списка словарей из списка объектов вакансий"""

        return [vacancy.to_dict() for vacancy in vacancies]

    @staticmethod
    def get_list_id_vacancies(vacancies: list) -> list:
        """Метод получения списка ID из списка вакансий"""

        return [vacancy.id if isinstance(vacancy, Vacancy) else vacancy["id"] for vacancy in vacancies]

    @staticmethod
    def get_top_salary_vacancies(vacancies: list, top_n: int) -> list:
        """Метод возвращает топ-n вакансий по зарплате"""

        return sorted(vacancies, reverse=True)[:top_n]

    @staticmethod
    def filter_by_keywords(vacancies: list, keywords: list) -> list:
        """Метод фильтрует вакансии, которые содержат ключевые слова в названии, требованиях или обязанностях"""

        filtered_vacancies = []
        for vacancy in vacancies:
            string_for_searching = (vacancy.name + str(vacancy.requirement) + str(vacancy.responsibility)).lower()
            check_status = True
            for keyword in keywords:
                if keyword.lower() not in string_for_searching:
                    check_status = False
            if check_status:
                filtered_vacancies.append(vacancy)
        return filtered_vacancies
