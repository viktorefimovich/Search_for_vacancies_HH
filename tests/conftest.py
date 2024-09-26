import pytest

from src.json_worker import JSONWorker


@pytest.fixture
def json_worker():
    """Фикстура для создания объекта JSONWorker"""

    return JSONWorker("test_file.json")
