class Vacancy:
    """Класс для работы с вакансиями"""
    __slots__ = ("name", "url_vacancy", "salary", "description")

    def __init__(self, name, url_vacancy, salary, description):
        """Метод инициализации объекта класса Vacancy"""

        self.name = name
        self.url_vacancy = url_vacancy
        self.salary = salary
        self.description = description

    def cast_to_object_list(self, vacancies):
        """Метод преобразования набора данных из JSON в список объектов"""

        ...
