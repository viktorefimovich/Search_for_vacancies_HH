from pathlib import Path
from typing import Union

from src.excel_worker import ExcelWorker
from src.json_worker import JSONWorker
from src.vacancy import Vacancy

ROOTPATH = Path(__file__).resolve().parent.parent


def get_file_data_info() -> list:
    """Функция возвращает список файлов с вакансиями в папке data"""

    path = Path(ROOTPATH, "data")
    files_list = []
    try:
        for file in path.iterdir():
            if file.is_file():
                files_list.append(file)
        print(f"В папке {path} содержится {len(files_list)} файл(а)(ов):")
    except OSError:
        print("Путь не является каталогом или по какой-то причине недоступен!")
        return []

    checked_files = []
    for file_ in files_list:
        try:
            checking_file: Union[JSONWorker, ExcelWorker]
            if file_.suffix.lower() == ".json":
                checking_file = JSONWorker(file_.name)
            elif file_.suffix.lower() == ".xlsx":
                checking_file = ExcelWorker(file_.name)
            else:
                continue

            file_data = checking_file.get_from_file()
            if len(file_data) == 0:
                raise TypeError
            vacancies = Vacancy.get_list_id_vacancies(file_data)
            checked_files.append(file_.name)
            print(f"{file_.name} - содержит {len(vacancies)} вакансий")
        except TypeError:
            print(f"{file_.name} - файл не содержит данных о вакансиях или формат файла не поддерживается")

    return checked_files
