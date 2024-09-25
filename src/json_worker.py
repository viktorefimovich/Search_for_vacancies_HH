import json
from pathlib import Path
from typing import Any

from src.abc_classes import FilesWork
from src.vacancy import Vacancy

ROOTPATH = Path(__file__).resolve().parent.parent


class JSONWorker(FilesWork):
    """Класс для работы с json файлами"""

    __file_name: str
    path_to_file: Path

    def __init__(self, file_name: str = "vacancies.json") -> None:
        """Метод инициализации объктов класса"""

        self.__file_name = self.__check_and_get_file_name(file_name)
        self.path_to_file = Path(ROOTPATH, "data", f"{self.__file_name}")

    def get_from_file(self) -> Any:
        """Метод для получения данных из файла"""

        try:
            with open(self.path_to_file, "r", encoding='utf-8') as file:
                vacancies = json.load(file)
                return vacancies
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_to_file(self, vacancies: list[dict]) -> None:
        """Метод для сохранения в файл списка вакансий"""

        with open(self.path_to_file, "w", encoding='utf-8') as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)

    def add_to_file(self, vacancies: list[dict]) -> None:
        """Метод для добавления в файл вакансий без дублирования"""

        vacancies_in_file = self.get_from_file()
        ids_vacancies = Vacancy.get_list_id_vacancies(vacancies)
        ids_vacancies_in_file = Vacancy.get_list_id_vacancies(vacancies_in_file)
        add_id_vacancies = list(set(ids_vacancies).difference(set(ids_vacancies_in_file)))
        for vacancy_id in add_id_vacancies:
            i = ids_vacancies.index(vacancy_id)
            vacancies_in_file.append(vacancies[i])

        self.save_to_file(vacancies_in_file)

    def delete_from_file(self) -> None:
        """Общий функционал для удаления данных из файла"""

        self.save_to_file([])

    @staticmethod
    def __check_and_get_file_name(file_name: str) -> str:
        """Метод проверки и получения имени файла"""

        if file_name[-5:] != ".json":
            return f"{file_name}.json"
        return file_name
