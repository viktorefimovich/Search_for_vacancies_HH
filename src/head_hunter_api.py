from src.abc_classes import APIParser


class HeadHunterAPI(APIParser):
    """Класс для ратобы с API сайта HH.ru"""

    def __init__(self):
        """Метод инициализации объекта класса"""

        ...

    def __get_vacancies(self, keyword):
        """Метод получения вакансий в формате JSON с API сайта по ключевому слову"""

        ...
