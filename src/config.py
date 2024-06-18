"""
Модуль настройки для считывания параметров подключения к базе данных из INI-файла и параметров работодателей для парсера.
"""

import os.path
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """
    Считывает конфигурацию из INI-файла и возвращает словарь параметров подключения к базе данных.

    :param filename: Путь к INI-файлу, содержащему сведения о подключении к базе данных.
    :param section: Раздел в INI-файле для чтения.
    :return: Словарь параметров подключения к базе данных.
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename)
        )
    return db


ROOT_DIR = os.path.dirname(__file__)
'''Параметры для парсера'''
hh_api_config = {'page': 0,
    'employer_id': [
        '3809',
        '1122462',
        '78638',
        '1740',
        '3776',
        '3127',
        '3529',
        '2104700',
        '15478',
        '4949',
        '2180'
    ],
    'per_page': 100,
    'area': 1,
    'only_with_salary': True
}
