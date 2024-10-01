import os
from tempfile import NamedTemporaryFile
from typing import Generator

import pytest

from src.json_worker import JSONWorker


@pytest.fixture
def json_worker() -> JSONWorker:
    """Фикстура для создания объекта JSONWorker"""

    return JSONWorker("test_file.json")


@pytest.fixture
def vacancy_data() -> dict:
    return {
        "id": 1,
        "name": "Software Engineer",
        "location": "Москва",
        "salary_from": 100000,
        "salary_to": 150000,
        "salary_string": "От 100000 до 150000",
        "published_at": "2024-01-01",
        "url": "http://example.com",
        "name_employer": "ExampleCompany",
        "experience": "3-5 лет",
        "requirement": "Python, Django",
        "responsibility": "Develop backend services",
    }


@pytest.fixture
def vacancy_data2() -> dict:
    return {
        "id": 2,
        "name": "Software Engineer",
        "location": "Москва",
        "salary_from": 120000,
        "salary_to": 150000,
        "salary_string": "От 100000 до 150000",
        "published_at": "2024-01-01",
        "url": "http://example.com",
        "name_employer": "ExampleCompany",
        "experience": "3-5 лет",
        "requirement": "Python, Django",
        "responsibility": "Develop backend services",
    }


@pytest.fixture
def vacancy_data3() -> dict:
    return {
        "id": 3,
        "name": "Software Engineer",
        "location": "Москва",
        "salary_from": 120000,
        "salary_to": 150000,
        "salary_string": "От 100000 до 150000",
        "published_at": "2024-01-01",
        "url": "http://example.com",
        "name_employer": "ExampleCompany",
        "experience": "3-5 лет",
        "requirement": "Python, Django",
        "responsibility": "Develop backend services",
    }


@pytest.fixture
def vacancy_data_none() -> dict:
    return {
        "id": 2,
        "name": None,
        "location": None,
        "salary_from": None,
        "salary_to": None,
        "salary_string": None,
        "published_at": None,
        "url": None,
        "name_employer": None,
        "experience": None,
        "requirement": None,
        "responsibility": None,
    }


@pytest.fixture
def partial_vacancy_data() -> dict:
    return {
        "id": 1,
        "name": "Software Engineer",
        "location": "Moscow",
        "salary_string": "Зарплата не указана",
        "published_at": "2023-01-01",
        "url": "http://example.com",
        "name_employer": "ExampleCompany",
    }


@pytest.fixture
def empty_vacancy_data() -> dict:
    return {}


@pytest.fixture
def vacancies_from_hh() -> list:
    return [
        {
            "id": "12345",
            "name": "Python Developer",
            "area": {"name": "Moscow"},
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "published_at": "2023-09-01T00:00:00",
            "alternate_url": "https://hh.ru/vacancy/12345",
            "employer": {"name": "Tech Company"},
            "experience": {"name": "3-5 лет"},
            "snippet": {"requirement": "Опыт работы с Python, Django", "responsibility": "Разработка веб-приложений"},
        },
        {
            "id": "67890",
            "name": "Data Scientist",
            "area": {"name": "Saint Petersburg"},
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "published_at": "2023-09-02T00:00:00",
            "alternate_url": "https://hh.ru/vacancy/67890",
            "employer": {"name": "Data Company"},
            "experience": {"name": "1-3 года"},
            "snippet": {
                "requirement": "Опыт работы с машинным обучением",
                "responsibility": "Анализ данных и построение моделей",
            },
        },
    ]


@pytest.fixture
def temp_excel_file() -> Generator:
    """Создает временный excel файл для тестирования"""

    with NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        yield tmp.name
    os.remove(tmp.name)
