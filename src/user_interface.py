import sys
from typing import Any

from src.excel_worker import ExcelWorker
from src.head_hunter_api import HeadHunterAPI
from src.json_worker import JSONWorker
from src.utils import get_file_data_info
from src.vacancy import Vacancy


class UI:
    """Класс для работы с пользователем"""

    @staticmethod
    def user_interaction() -> None:
        """Функция взаимодействия с пользователем"""

        print("Выберите действие:")
        print("1. Загрузить данные о вакансиях с сайта hh.ru по ключевому слову")
        print("2. Получить инф-ю о ранее загруженных данных (хранятся в 'data/', поддерживаемые форматы: json, xlsx)")
        print("q. Выход из программы")
        choice = None
        while choice not in ["1", "2", "q"]:
            choice = input("Введите 1 или 2 или q для выхода: ")

        match choice:
            case "1":
                UI.get_vacancies_HH()
            case "2":
                UI.files_info_and_choice()
            case "q":
                sys.exit()

    @staticmethod
    def get_vacancies_HH() -> Any:
        """Функция для загрузки вакансий с сайта HH.ru"""

        query = input("Введите ключевое слово для поиска вакансий: ")
        vacancies = HeadHunterAPI.get_vacancies(query)
        vacancies_list = Vacancy.vacancies_from_hh_processing(vacancies)
        vacancies_objects = Vacancy.get_list_of_vacancies(vacancies_list)
        if len(vacancies_objects) == 0:
            print("Вакансий по вашему запросу не найдено, попробуйте снова")
            return UI.get_vacancies_HH()
        print()
        print(f"Количество загруженных вакансий - {len(vacancies_objects)}")
        print()
        return UI.vacancies_working(vacancies_objects)

    @staticmethod
    def files_info_and_choice() -> None:
        """Получение данных о файлах с вакансиями"""

        files = get_file_data_info()
        if len(files) == 0:
            print("Доступные для работы файлы отсутствуют\n")
            return UI.user_interaction()
        else:
            print("Для дальнейшей работы доступны следующие файлы: ")
            for i in range(len(files)):
                print(f"{i + 1}. {files[i]}")
            file_for_work = input("Введите имя файла для загрузки: ")
            while file_for_work not in files:
                file_for_work = input("Вы ввели неверное имя файла! Повторите ввод: ")

            UI.file_working(file_for_work)

    @staticmethod
    def file_working(file_name: str) -> Any:
        """Функция интерфейса для выбора опций загрузки данных о вакансиях из файла"""

        file_worker = None
        if file_name[-5:] == ".json":
            file_worker = JSONWorker(file_name)
        elif file_name[-5:] == ".xlsx":
            file_worker = ExcelWorker(file_name)

        print("Выберите действие с файлом:")
        print("1. Загрузить все вакансии из файла")
        print("2. Очистить файл")
        choice = 0
        while choice not in [1, 2]:
            choice = int(input("Выберите 1 или 2: "))
        match choice:
            case 1:
                vacancies_list = file_worker.get_from_file()
                vacancies_objects = Vacancy.get_list_of_vacancies(vacancies_list)
                print(f"Количество загруженных вакансий - {len(vacancies_objects)}")
                return UI.vacancies_working(vacancies_objects)

            case 2:
                file_worker.delete_from_file()
                print("Файл очищен")
                return UI.files_info_and_choice()

    @staticmethod
    def vacancies_working(vacancies: list) -> None:
        """Обработка списка вакансий"""

        print("Выберите действие для списка вакансий:")
        print("1. Cохранить в файл")
        print("2. Отфильтровать топ вакансий по зарплате")
        print("3. Отфильтровать вакансии по ключевым словам")
        print("4. Вывести краткую информацию о вакансиях в консоль")
        print("5. Выход из программы")
        choice = 0
        while choice not in [1, 2, 3, 4, 5]:
            try:
                choice = int(input("Введите цифру от 1 до 5 для выбора действия: "))
            except ValueError:
                print("Повторите ввод - укажите целое число от 1 до 5")

        match choice:

            case 1:
                UI.save_to_file(vacancies)
                return UI.vacancies_working(vacancies)

            case 2:
                while True:
                    try:
                        n = int(input("Введите кол-во вакансий , которые надо отобрать из списка: "))
                    except ValueError:
                        print("Повторите ввод - укажите целое число")
                    else:
                        if n <= 0:
                            print("Число должно быть больше 0. Давайте попробуем ещё раз")
                        else:
                            break
                top_vacancies = Vacancy.get_top_salary_vacancies(vacancies, n)
                return UI.vacancies_working(top_vacancies)

            case 3:
                keyword_list = input("Введите ключевые слова для фильтрации через пробел: ").strip().split()
                filtered_vacancy = Vacancy.filter_by_keywords(vacancies, keyword_list)
                if len(filtered_vacancy) == 0:
                    print("По вашему запросу ничего не найдено. Давайте попробуем ещё раз")
                    return UI.vacancies_working(vacancies)
                return UI.vacancies_working(filtered_vacancy)

            case 4:
                for vacancy in vacancies:
                    print(vacancy)
                print()
                return UI.vacancies_working(vacancies)

            case 5:
                sys.exit()

    @staticmethod
    def save_to_file(vacancies: list) -> None:
        """Функция для сохранения данных в файл"""

        file_name = input("Введите имя файла для сохраниния (имя по умолчанию - vacancies): ")
        vacancies_to_save = Vacancy.get_list_of_dicts_vacancies(vacancies)
        if len(file_name) > 0:
            json_saver = JSONWorker(file_name)
        else:
            json_saver = JSONWorker()
            file_name = "vacancies"
        try:
            json_saver.add_to_file(vacancies_to_save)
            print(f"Данные успешно добавлены в файл {file_name}.json")
        except (FileNotFoundError, KeyError, TypeError):
            json_saver.save_to_file(vacancies_to_save)
            print(f"Данные успешно сохранены в файл {file_name}.json")
