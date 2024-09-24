from pathlib import Path
from typing import Any

import pandas as pd


from src.abc_classes import FilesWork

ROOTPATH = Path(__file__).resolve().parent.parent


class ExcelWorker(FilesWork):
    """Класс для работы с excel-файлами"""

    __file_name: str
    path_to_file: Path

    def __init__(self, file_name: str = "vacancies.xlsx") -> None:
        self.__file_name = self.__check_and_get_file_name(file_name)
        self.path_to_file = Path(ROOTPATH, f"{self.__file_name}")

    def save_to_file(self, vacancies: list[dict]) -> None:
        """Метод для сохранения в файл списка вакансий"""

        pd.DataFrame(vacancies).to_excel(self.path_to_file, index=False)

    def add_to_file(self, vacancies: list[dict]) -> None:
        """Метод для добавления в файл вакансий без дублирования"""

        vacancies_in_file = pd.read_excel(self.path_to_file)
        vacancies_in_file["id"] = vacancies_in_file["id"].astype(str)
        vacancies_to_add = pd.DataFrame(vacancies)
        vacancies_to_file = pd.concat([vacancies_in_file, vacancies_to_add], ignore_index=True).drop_duplicates(
            subset=["id"]
        )
        vacancies_to_file.to_excel(self.path_to_file, index=False)

    def get_from_file(self) -> Any:
        """Метод для получения данных из файла"""

        df = pd.read_excel(self.path_to_file)
        return df.to_dict(orient="records")

    def delete_from_file(self) -> None:
        """Метод удаляет все данные из файла"""

        pd.DataFrame().to_excel(self.path_to_file, index=False)

    @staticmethod
    def __check_and_get_file_name(file_name: str) -> str:
        """Метод возвращает имя excel-файла"""

        if file_name[-5:] != ".xlsx":
            return f"{file_name}.xlsx"
        return file_name
