import pandas as pd

from src.excel_worker import ExcelWorker


def test_save_to_file(temp_excel_file: str) -> None:
    """Тест метода save_to_file: сохранение списка вакансий в файл"""

    worker = ExcelWorker(file_name=temp_excel_file)

    vacancies = [
        {"id": "1", "name": "Python Developer", "salary": 100000},
        {"id": "2", "name": "Java Developer", "salary": 120000},
    ]

    worker.save_to_file(vacancies)

    df = pd.read_excel(worker.path_to_file)
    assert len(df) == 2
    assert df.iloc[0]["name"] == "Python Developer"
    assert df.iloc[1]["salary"] == 120000


def test_add_to_file(temp_excel_file: str) -> None:
    """Тест метода add_to_file: добавление новых вакансий без дублирования"""

    worker = ExcelWorker(file_name=temp_excel_file)

    initial_vacancies = [
        {"id": "1", "name": "Python Developer", "salary": 100000},
        {"id": "2", "name": "Java Developer", "salary": 120000},
    ]
    worker.save_to_file(initial_vacancies)

    new_vacancies = [
        {"id": "2", "name": "Java Developer", "salary": 130000},  # дубликат
        {"id": "3", "name": "Go Developer", "salary": 110000},    # новая вакансия
    ]

    new_vacancies = [{**vacancy, "id": str(vacancy["id"])} for vacancy in new_vacancies]

    worker.add_to_file(new_vacancies)

    df = pd.read_excel(worker.path_to_file)

    df["id"] = df["id"].astype(str)

    assert len(df) == 3
    assert df[df["id"] == "3"]["name"].values[0] == "Go Developer"
    assert df[df["id"] == "2"]["salary"].values[0] == 120000


def test_get_from_file(temp_excel_file: str) -> None:
    """Тест метода get_from_file: получение данных из файла"""

    worker = ExcelWorker(file_name=temp_excel_file)

    vacancies = [
        {"id": "1", "name": "Python Developer", "salary": 100000},
        {"id": "2", "name": "Java Developer", "salary": 120000},
    ]

    worker.save_to_file(vacancies)
    vacancies_from_file = worker.get_from_file()

    assert len(vacancies_from_file) == 2
    assert vacancies_from_file[0]["name"] == "Python Developer"
    assert vacancies_from_file[1]["salary"] == 120000


def test_delete_from_file(temp_excel_file: str) -> None:
    """Тест метода delete_from_file: удаление всех данных из файла"""

    worker = ExcelWorker(file_name=temp_excel_file)

    vacancies = [
        {"id": "1", "name": "Python Developer", "salary": 100000},
        {"id": "2", "name": "Java Developer", "salary": 120000},
    ]

    worker.save_to_file(vacancies)
    worker.delete_from_file()

    df = pd.read_excel(worker.path_to_file)
    assert df.empty
