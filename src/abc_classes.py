from abc import ABC, abstractmethod
from typing import Any


class APIParser(ABC):
    """Абстрактный класс для работы с API сайта"""

    @abstractmethod
    def get_vacancies(self, keyword: str, page: int = 0, per_page: int = 100) -> Any:
        """Абстрактный метод получения вакансий с API сайта по ключевому слову"""

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
