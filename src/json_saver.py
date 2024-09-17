from src.abc_classes import FilesWork


class JSONSaver(FilesWork):
    """Класс для работы с информацией о вакансиях"""

    def __init__(self, name):
        """Метод инициализации объекта класса"""

        self.__name = name

    def get_vacancy(self):
        """Метод получения вакансий"""

        ...

    def add_vacancy(self):
        """Метод добавления вакансии"""
        ...

    def delete_vacancy(self):
        """Метод удаления вакансии"""
        ...
