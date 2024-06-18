from abc import ABC, abstractmethod
from config import hh_api_config
import requests


class Parser(ABC):
    """
    Абстрактный класс для работы с API HeadHunter
    """

    @abstractmethod
    def get_vacancies_data(self, *args, **kwargs):
        """
        Метод для загрузки ваканский с заданными параметрами
        """
        pass

    @abstractmethod
    def get_employers_data(self, *args, **kwargs):
        """
        Метод для загрузки работодателей с заданными параметрами
        """
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter
    Подготавливает параметры запроса и выбирает вакансии на основе поискового запроса.
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'page': 0,
                       'employer_id': hh_api_config.get('employer_id'),
                       'per_page': 100,
                       'area': 1,
                       'only_with_salary': True
                       }
        self.vacancies = []

    def get_vacancies_data(self):
        """
        Метод для загрузки ваканский с заданными параметрами
        """
        while self.params.get('page') != 5:
            response = requests.get(self.__url, headers=self.headers, params=self.params)
            if response.status_code != 200:
                break
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
        return self.vacancies

    def get_employers_data(self):
        """
        Метод для загрузки работодателей с заданными параметрами
        """
        employers_data = []
        for employer in hh_api_config.get('employer_id'):
            url = f'https://api.hh.ru/employers/{employer}'
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                break
            employer_data = {
                'id': response.json()['id'],
                'name': response.json()['name'],
                'url': response.json()['alternate_url'],
            }
            employers_data.append(employer_data)
        return employers_data
