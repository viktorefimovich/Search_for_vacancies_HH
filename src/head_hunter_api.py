from typing import Any

import requests

from src.abc_classes import APIParser


class HeadHunterAPI(APIParser):
    """Класс для ратобы с API сайта HH.ru"""

    @staticmethod
    def __connect(params: dict) -> Any:
        """Метод подключения к API HH.ru"""

        try:
            url = "https://api.hh.ru/vacancies"
            headers = {"User-Agent": "HH-User-Agent"}
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                raise ConnectionError(f"Не удалось подключиться к API hh.ru. Код ошибки: {response.status_code}")
            return response
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            raise

    @classmethod
    def get_vacancies(cls, keyword: str, max_pages: int = 20) -> list:
        """Метод получения вакансий в формате JSON с API сайта по ключевому слову"""

        params: dict = {"text": keyword, "page": 0, "per_page": 100}
        vacancies = []
        while params["page"] < max_pages:
            print("-", end="")
            vacancies_page = cls.__connect(params).json()["items"]
            vacancies.extend(vacancies_page)
            params["page"] += 1
        return vacancies
