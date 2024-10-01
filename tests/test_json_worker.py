import json
from typing import Any
from unittest.mock import mock_open, patch

import pytest

from src.json_worker import JSONWorker


def test_get_from_file_empty_file(json_worker: JSONWorker) -> None:
    """Тест: метод возвращает пустой список, если файл пустой"""

    empty_file_data = ""

    with patch("builtins.open", mock_open(read_data=empty_file_data)) as mock_file:
        result = json_worker.get_from_file()
        assert result == []
        mock_file.assert_called_once_with(json_worker.path_to_file, "r", encoding="utf-8")


def test_get_from_file_invalid_json(json_worker: JSONWorker) -> None:
    """Тест: метод возвращает пустой список, если файл содержит некорректный JSON (JSONDecodeError)"""

    invalid_json_data = "{invalid_json: true}"

    with patch("builtins.open", mock_open(read_data=invalid_json_data)) as mock_file:
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = json_worker.get_from_file()
            assert result == []
            mock_file.assert_called_once_with(json_worker.path_to_file, "r", encoding="utf-8")


def test_get_from_file_file_not_found(json_worker: JSONWorker) -> None:
    """Тест: метод возвращает пустой список, если файл не существует (FileNotFoundError)"""

    with patch("builtins.open", side_effect=FileNotFoundError) as mock_file:
        result = json_worker.get_from_file()
        assert result == []
        mock_file.assert_called_once_with(json_worker.path_to_file, "r", encoding="utf-8")


def test_get_from_file_with_data(json_worker: JSONWorker) -> None:
    """Тестируем, что метод get_from_file возвращает данные из файла"""

    data = [{"id": "12345", "title": "Python Developer"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(data))) as mock_file:
        result = json_worker.get_from_file()
        assert result == data
        mock_file.assert_called_once_with(json_worker.path_to_file, "r", encoding="utf-8")


def test_get_from_file_with_valid_data(json_worker: JSONWorker) -> None:
    """Тест: метод возвращает данные, если файл существует и содержит валидный JSON"""

    test_data = [{"id": "1", "title": "Developer"}, {"id": "2", "title": "Designer"}]

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))) as mock_file:
        result = json_worker.get_from_file()
        assert result == test_data
        mock_file.assert_called_once_with(json_worker.path_to_file, "r", encoding="utf-8")


def test_save_to_file(json_worker: JSONWorker) -> None:
    """Тестируем, что метод save_to_file сохраняет данные в файл"""

    vacancies = [{"id": "12345", "title": "Python Developer"}]
    with patch("builtins.open", mock_open()) as mock_file:
        json_worker.save_to_file(vacancies)
        mock_file.assert_called_once_with(json_worker.path_to_file, "w", encoding="utf-8")


@patch("src.vacancy.Vacancy.get_list_id_vacancies", return_value=["123"])
def test_add_to_file_no_duplicates(mock_get_list_id_vacancies: Any, json_worker: JSONWorker) -> None:
    """Тестируем, что метод add_to_file не добавляет дублирующиеся вакансии"""
    vacancies = [{"id": "123", "title": "Python Developer"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(vacancies))):
        json_worker.add_to_file(vacancies)
        mock_get_list_id_vacancies.assert_called()


def test_delete_from_file(json_worker: JSONWorker) -> None:
    """Тестируем, что метод delete_from_file очищает файл"""

    with patch("builtins.open", mock_open()) as mock_file:
        json_worker.delete_from_file()
        mock_file.assert_called_once_with(json_worker.path_to_file, "w", encoding="utf-8")


@pytest.mark.parametrize(
    "vacancies, new_vacancies, expected_output",
    [
        ([], [], []),
        ([{"id": 1}], [{"id": 2}], [{"id": 1}, {"id": 2}]),
        ([{"id": 1}, {"id": 7}], [{"id": 2}, {"id": 7}], [{"id": 1}, {"id": 7}, {"id": 2}]),
    ],
)
def test_JSONWorker_add_to_file(tmpdir: Any, vacancies: list, new_vacancies: list, expected_output: list) -> None:
    """Тест для метода add_to_file"""

    temp_file = tmpdir.join("vacancies.json")

    initial_data = json.dumps(vacancies)
    temp_file.write(initial_data)

    worker = JSONWorker(temp_file.strpath)
    worker.add_to_file(new_vacancies)

    actual_data = json.loads(temp_file.read())
    assert actual_data == expected_output
