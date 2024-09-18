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
                raise ConnectionError("Не удалось подключиться к API hh.ru")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    @classmethod
    def get_vacancies(cls, keyword: str) -> Any:
        """Метод получения вакансий в формате JSON с API сайта по ключевому слову"""

        params = {"text": keyword, "page": 0, "per_page": 100}
        vacancies = []
        while params.get("page") != 20:
            print("#", end="")
            vacancies_page = cls.__connect(params).json()["items"]
            vacancies.extend(vacancies_page)
            params["page"] += 1
        return vacancies

# if __name__ == "__main__":
#     hh_api = HeadHunterAPI()
#     print(hh_api.get_vacancies("Python", per_page=1))
