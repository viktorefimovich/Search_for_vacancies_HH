import pytest

from src.json_worker import JSONWorker


@pytest.fixture
def json_worker():
    """Фикстура для создания объекта JSONWorker"""

    return JSONWorker("test_file.json")


@pytest.fixture
def vacancy_data():
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
        "responsibility": "Develop backend services"
    }
