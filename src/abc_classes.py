from abc import ABC, abstractmethod
from typing import Any


class APIParser(ABC):
    """Абстрактный класс для работы с API сайта"""

    @staticmethod
    @abstractmethod
    def __connect(params: dict) -> Any:
        """Приватный метод для подключения к API"""

        pass

    @classmethod
    @abstractmethod
    def get_vacancies(cls, keyword: str) -> list:
        """Метод для получения вакансий по ключевому слову"""

        pass


class FilesWork(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def get_vacancy(self) -> Any:
        """Абстрактный метод получения данных из файла"""

        ...

    @abstractmethod
    def add_vacancy(self) -> Any:
        """Абстрактный метолд добавления данных в файл"""

        ...

    @abstractmethod
    def delete_vacancy(self) -> Any:
        """Абстрактный метолд удаления данных из файла"""

        ...
