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
    def save_to_file(self, vacancies: list[dict]) -> None:
        """Метод для сохранения в файл списка вакансий"""

        pass

    @abstractmethod
    def add_to_file(self, vacancies: list[dict]) -> None:
        """Метод для добавления в файл вакансий без дублирования"""

        pass

    @abstractmethod
    def get_from_file(self) -> list[dict]:
        """Метод для получения данных из файла"""

        pass

    @abstractmethod
    def delete_from_file(self) -> None:
        """Общий функционал для удаления данных из файла"""

        pass
