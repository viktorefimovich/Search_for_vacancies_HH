from typing import Any

import requests

from src.abc_classes import APIParser


class HeadHunterAPI(APIParser):
    """Класс для ратобы с API сайта HH.ru"""

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        """Метод инициализации объекта класса"""

        self.__connect()

    def __connect(self) -> Any:
        """Метод подключения к API HH.ru"""

        try:
            response = requests.get(self.BASE_URL)
            if response.status_code != 200:
                raise ConnectionError("Не удалось подключиться к API hh.ru")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def get_vacancies(self, keyword: str, page: int = 0, per_page: int = 100) -> Any:
        """Метод получения вакансий в формате JSON с API сайта по ключевому слову"""

        params = {
            "text": keyword,
            "page": page,
            "per_page": per_page
        }
        self.__connect()
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception(f"Ошибка получения данных: {response.status_code}")


# if __name__ == "__main__":
#     hh_api = HeadHunterAPI()
#     print(hh_api.get_vacancies("Python"))
