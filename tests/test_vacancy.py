import pytest

from src.vacancy import Vacancy


def test_vacancy_init(vacancy_data: dict) -> None:
    """Тест для инициализации объекта"""

    vacancy = Vacancy(vacancy_data)

    assert vacancy.id == vacancy_data["id"]
    assert vacancy.name == vacancy_data["name"]
    assert vacancy.location == vacancy_data["location"]
    assert vacancy.salary_from == vacancy_data["salary_from"]
    assert vacancy.salary_to == vacancy_data["salary_to"]
    assert vacancy.salary_string == vacancy_data["salary_string"]
    assert vacancy.url == vacancy_data["url"]


def test_vacancy_init_partial(partial_vacancy_data: dict) -> None:
    """Тест для частично отсутствующих атрибутов"""

    vacancy = Vacancy(partial_vacancy_data)

    assert vacancy.id == partial_vacancy_data["id"]
    assert vacancy.name == partial_vacancy_data["name"]
    assert vacancy.location == partial_vacancy_data["location"]
    assert vacancy.salary_from is None
    assert vacancy.salary_to is None
    assert vacancy.salary_string == partial_vacancy_data["salary_string"]
    assert vacancy.published_at == partial_vacancy_data["published_at"]
    assert vacancy.url == partial_vacancy_data["url"]
    assert vacancy.name_employer == partial_vacancy_data["name_employer"]
    assert vacancy.experience is None
    assert vacancy.requirement is None
    assert vacancy.responsibility is None


def test_vacancy_init_empty(empty_vacancy_data: dict) -> None:
    """Тест для полностью отсутствующих атрибутов (пустой словарь)"""

    vacancy = Vacancy(empty_vacancy_data)

    assert vacancy.id is None
    assert vacancy.name is None
    assert vacancy.location is None
    assert vacancy.salary_from is None
    assert vacancy.salary_to is None
    assert vacancy.salary_string is None
    assert vacancy.published_at is None
    assert vacancy.url is None
    assert vacancy.name_employer is None
    assert vacancy.experience is None
    assert vacancy.requirement is None
    assert vacancy.responsibility is None


def test_vacancy_init_invalid_keys() -> None:
    """Тест на некорректные данные"""

    invalid_data = {"invalid_key": "value", "id": 1, "name": "Software Engineer"}

    vacancy = Vacancy(invalid_data)

    assert vacancy.id == 1
    assert vacancy.name == "Software Engineer"
    assert vacancy.location is None
    assert not hasattr(vacancy, "invalid_key")


def test_vacancy_str(vacancy_data: dict) -> None:
    """Тест для проверки строки вывода __str__"""

    vacancy = Vacancy(vacancy_data)
    expected_str = (
        f"{vacancy_data['name']} - Зарплата: {vacancy_data['salary_string']} - "
        f"Город: {vacancy_data['location']}- Ссылка на вакансию: {vacancy_data['url']}"
    )

    assert str(vacancy) == expected_str


def test_vacancy_comparison(vacancy_data: dict, vacancy_data2: dict, vacancy_data3: dict) -> None:
    """Тесты для операций сравнения по зарплате"""

    vacancy1 = Vacancy(vacancy_data)
    vacancy2 = Vacancy(vacancy_data2)
    vacancy3 = Vacancy(vacancy_data3)

    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 != vacancy2
    assert vacancy2 == vacancy3
    assert vacancy2 >= vacancy3
    assert vacancy2 <= vacancy3


def test_vacancy_comparison_type_error(vacancy_data: dict) -> None:
    """Тест на исключение TypeError при сравнении с некорректным типом"""

    vacancy = Vacancy(vacancy_data)
    with pytest.raises(TypeError):
        vacancy == "not a vacancy"
    with pytest.raises(TypeError):
        vacancy < "not a vacancy"
    with pytest.raises(TypeError):
        vacancy > 12345
    with pytest.raises(TypeError):
        vacancy != 100000
    with pytest.raises(TypeError):
        vacancy <= 90000
    with pytest.raises(TypeError):
        vacancy >= 110000


def test_get_salary(vacancy_data: dict) -> None:
    """Тест для метода get_salary"""

    vacancy = Vacancy(vacancy_data)
    assert vacancy.get_salary() == "От 100000 до 150000"


def test_get_list_of_vacancies(vacancy_data: dict) -> None:
    """Тест для метода get_list_of_vacancies"""

    vacancies_list = [vacancy_data]
    vacancies = Vacancy.get_list_of_vacancies(vacancies_list)

    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].id == vacancy_data["id"]


def test_get_list_id_vacancies(vacancy_data: dict) -> None:
    """Тест для метода get_list_id_vacancies"""

    vacancies_list = [vacancy_data]
    vacancies = Vacancy.get_list_of_vacancies(vacancies_list)
    ids = Vacancy.get_list_id_vacancies(vacancies)

    assert ids == [vacancy_data["id"]]


def test_get_top_salary_vacancies(vacancy_data: dict, vacancy_data2: dict) -> None:
    """Тест для метода get_top_salary_vacancies"""

    vacancy1 = Vacancy(vacancy_data)
    vacancy2 = Vacancy(vacancy_data2)

    vacancies = [vacancy1, vacancy2]
    top_vacancies = Vacancy.get_top_salary_vacancies(vacancies, 1)

    assert len(top_vacancies) == 1
    assert top_vacancies[0].salary_from == 120000


def test_filter_by_keywords(vacancy_data: dict) -> None:
    """Тест для метода filter_by_keywords"""

    vacancy = Vacancy(vacancy_data)
    keywords = ["Python", "Develop"]

    filtered = Vacancy.filter_by_keywords([vacancy], keywords)

    assert len(filtered) == 1
    assert filtered[0].name == vacancy_data["name"]

    keywords = ["Java"]
    filtered = Vacancy.filter_by_keywords([vacancy], keywords)

    assert len(filtered) == 0


def test_to_dict(vacancy_data: dict) -> None:
    """Тест для метода to_dict"""

    vacancy = Vacancy(vacancy_data)

    # Ожидаемый результат
    expected_dict = {
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

    assert vacancy.to_dict() == expected_dict


def test_to_dict_with_none_values(vacancy_data_none: dict) -> None:
    """Тест для случая, когда некоторые атрибуты None"""

    vacancy = Vacancy(vacancy_data_none)

    expected_dict = {
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

    assert vacancy.to_dict() == expected_dict


def test_get_list_of_dicts_vacancies(vacancy_data: dict, vacancy_data2: dict) -> None:
    """Тест для метода get_list_of_dicts_vacancies"""

    vacancy1 = Vacancy(vacancy_data)
    vacancy2 = Vacancy(vacancy_data2)

    vacancies = [vacancy1, vacancy2]

    expected_list_of_dicts = [
        {
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
        },
        {
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
        },
    ]

    result = Vacancy.get_list_of_dicts_vacancies(vacancies)
    assert result == expected_list_of_dicts


def test_get_list_of_dicts_vacancies_empty_list() -> None:
    """Тест для случая, когда список объектов вакансий пуст"""

    vacancies = []
    expected_list_of_dicts = []

    result = Vacancy.get_list_of_dicts_vacancies(vacancies)
    assert result == expected_list_of_dicts


def test_vacancies_from_hh_processing(vacancies_from_hh: list) -> None:
    """Тест для метода vacancies_from_hh_processing"""

    processed_vacancies = Vacancy.vacancies_from_hh_processing(vacancies_from_hh)

    assert processed_vacancies == [
        {
            "id": "12345",
            "name": "Python Developer",
            "location": "Moscow",
            "salary_from": 100000,
            "salary_to": 150000,
            "salary_string": "От 100000 до 150000",
            "published_at": "2023-09-01T00:00:00",
            "url": "https://hh.ru/vacancy/12345",
            "name_employer": "Tech Company",
            "experience": "3-5 лет",
            "requirement": "Опыт работы с Python, Django",
            "responsibility": "Разработка веб-приложений",
        },
        {
            "id": "67890",
            "name": "Data Scientist",
            "location": "Saint Petersburg",
            "salary_from": 120000,
            "salary_to": 180000,
            "salary_string": "От 120000 до 180000",
            "published_at": "2023-09-02T00:00:00",
            "url": "https://hh.ru/vacancy/67890",
            "name_employer": "Data Company",
            "experience": "1-3 года",
            "requirement": "Опыт работы с машинным обучением",
            "responsibility": "Анализ данных и построение моделей",
        },
    ]


def test_vacancies_from_hh_processing_empty_list() -> None:
    """Тест для случая с пустым списком вакансий"""

    vacancies = []
    result = Vacancy.vacancies_from_hh_processing(vacancies)

    assert result == []
