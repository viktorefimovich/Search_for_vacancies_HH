import json
from unittest.mock import patch, mock_open

import pytest

from src.json_worker import JSONWorker


def test_get_from_file_empty_file(json_worker):
    """Тест: метод возвращает пустой список, если файл пустой"""

    empty_file_data = ""

    with patch("builtins.open", mock_open(read_data=empty_file_data)) as mock_file:
        result = json_worker.get_from_file()
        assert result == []
        mock_file.assert_called_once_with(json_worker.path_to_file, 'r', encoding='utf-8')


def test_get_from_file_invalid_json(json_worker):
    """Тест: метод возвращает пустой список, если файл содержит некорректный JSON (JSONDecodeError)"""

    invalid_json_data = "{invalid_json: true}"

    with patch("builtins.open", mock_open(read_data=invalid_json_data)) as mock_file:
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            result = json_worker.get_from_file()
            assert result == []
            mock_file.assert_called_once_with(json_worker.path_to_file, 'r', encoding='utf-8')


def test_get_from_file_file_not_found(json_worker):
    """Тест: метод возвращает пустой список, если файл не существует (FileNotFoundError)"""

    with patch("builtins.open", side_effect=FileNotFoundError) as mock_file:
        result = json_worker.get_from_file()
        assert result == []
        mock_file.assert_called_once_with(json_worker.path_to_file, 'r', encoding='utf-8')


def test_get_from_file_with_data(json_worker):
    """Тестируем, что метод get_from_file возвращает данные из файла"""

    data = [{'id': '12345', 'title': 'Python Developer'}]
    with patch("builtins.open", mock_open(read_data=json.dumps(data))) as mock_file:
        result = json_worker.get_from_file()
        assert result == data
        mock_file.assert_called_once_with(json_worker.path_to_file, 'r', encoding='utf-8')


def test_get_from_file_with_valid_data(json_worker):
    """Тест: метод возвращает данные, если файл существует и содержит валидный JSON"""

    test_data = [{'id': '1', 'title': 'Developer'}, {'id': '2', 'title': 'Designer'}]

    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))) as mock_file:
        result = json_worker.get_from_file()
        assert result == test_data
        mock_file.assert_called_once_with(json_worker.path_to_file, 'r', encoding='utf-8')


def test_save_to_file(json_worker):
    """Тестируем, что метод save_to_file сохраняет данные в файл"""

    vacancies = [{'id': '12345', 'title': 'Python Developer'}]
    with patch("builtins.open", mock_open()) as mock_file:
        json_worker.save_to_file(vacancies)
        mock_file.assert_called_once_with(json_worker.path_to_file, 'w', encoding='utf-8')


@patch("src.vacancy.Vacancy.get_list_id_vacancies", return_value=['123'])
def test_add_to_file_no_duplicates(mock_get_list_id_vacancies, json_worker):
    """Тестируем, что метод add_to_file не добавляет дублирующиеся вакансии"""
    vacancies = [{'id': '123', 'title': 'Python Developer'}]
    with patch("builtins.open", mock_open(read_data=json.dumps(vacancies))):
        json_worker.add_to_file(vacancies)
        mock_get_list_id_vacancies.assert_called()


def test_delete_from_file(json_worker):
    """Тестируем, что метод delete_from_file очищает файл"""
    with patch("builtins.open", mock_open()) as mock_file:
        json_worker.delete_from_file()
        mock_file.assert_called_once_with(json_worker.path_to_file, 'w', encoding='utf-8')


def test_check_and_get_file_name_with_json_extension(json_worker):
    """Тест: если имя файла уже содержит .json, оно возвращается без изменений"""

    file_name = "vacancies.json"
    result = json_worker._JSONWorker__check_and_get_file_name(file_name)
    assert result == file_name


def test_check_and_get_file_name_without_json_extension(json_worker):
    """Тест: если имя файла не содержит .json, расширение должно добавиться"""

    file_name = "vacancies"
    result = json_worker._JSONWorker__check_and_get_file_name(file_name)
    assert result == "vacancies.json"


def test_check_and_get_file_name_with_empty_string(json_worker):
    """Тест: если имя файла пустое, метод должен корректно добавить .json"""

    file_name = ""
    result = json_worker._JSONWorker__check_and_get_file_name(file_name)
    assert result == ".json"


def test_check_and_get_file_name_short_name(json_worker):
    """Тест: если имя файла меньше 5 символов, метод должен корректно обработать"""

    file_name = "vac"
    result = json_worker._JSONWorker__check_and_get_file_name(file_name)
    assert result == "vac.json"


@pytest.mark.parametrize("vacancies, new_vacancies, expected_output", [
    ([], [], []),
    ([{"id": 1}], [{"id": 2}], [{"id": 1}, {"id": 2}]),
    ([{"id": 1}, {"id": 7}], [{"id": 2}, {"id": 7}], [{"id": 1}, {"id": 7}, {"id": 2}])
])
def test_JSONWorker_add_to_file(tmpdir, vacancies, new_vacancies, expected_output):
    temp_file = tmpdir.join("vacancies.json")

    initial_data = json.dumps(vacancies)
    temp_file.write(initial_data)

    worker = JSONWorker(temp_file.strpath)
    worker.add_to_file(new_vacancies)

    actual_data = json.loads(temp_file.read())
    assert actual_data == expected_output
