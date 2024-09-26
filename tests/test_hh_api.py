from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.head_hunter_api import HeadHunterAPI


@patch("src.head_hunter_api.requests.get")
def test_connect_success(mock_get: Any) -> None:
    """Тест успешного подключения к API HH.ru"""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    params = {"text": "Python", "page": 0, "per_page": 100}
    response = HeadHunterAPI._HeadHunterAPI__connect(params)

    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        headers={"User-Agent": "HH-User-Agent"},
        params=params
    )
    assert response.status_code == 200


@patch("src.head_hunter_api.requests.get")
def test_connect_failure(mock_get: Any) -> None:
    """Тест неудачного подключения к API HH.ru"""

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    params = {"text": "Python", "page": 0, "per_page": 100}
    with pytest.raises(ConnectionError):
        HeadHunterAPI._HeadHunterAPI__connect(params)


@patch("src.head_hunter_api.HeadHunterAPI._HeadHunterAPI__connect")
def test_get_vacancies(mock_connect: Any) -> None:
    """Тест метода get_vacancies для получения списка вакансий"""

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": 100000},
            {"id": "2", "name": "Data Scientist", "salary": 150000},
        ]
    }
    mock_connect.return_value = mock_response
    vacancies = HeadHunterAPI.get_vacancies("Python", max_pages=1)

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["name"] == "Data Scientist"
    mock_connect.assert_called_once()


@patch("src.head_hunter_api.HeadHunterAPI._HeadHunterAPI__connect")
def test_get_vacancies_multiple_pages(mock_connect: Any) -> None:
    """Тест метода get_vacancies для получения списка вакансий с нескольких страниц"""

    mock_response_page_1 = MagicMock()
    mock_response_page_1.json.return_value = {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": 100000},
        ]
    }
    mock_response_page_2 = MagicMock()
    mock_response_page_2.json.return_value = {
        "items": [
            {"id": "2", "name": "Data Scientist", "salary": 150000},
        ]
    }

    mock_connect.side_effect = [mock_response_page_1, mock_response_page_2]
    vacancies = HeadHunterAPI.get_vacancies("Python", max_pages=2)

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Developer"
    assert vacancies[1]["name"] == "Data Scientist"
    assert mock_connect.call_count == 2
