from src.hhparser import HeadHunterAPI
from src.config import config
from src.db_manager import DBManager
from src.utils import DBConnection, create_tables, truncate_tables, insert_companies, insert_vacancies


def main():
    """
    Основная функция, которая управляет процессом очистки и хранения.
    """
    params = config()
    db_conn = DBConnection('cw5', params).conn
    create_tables(db_conn)

    hh = HeadHunterAPI()
    vacancies_data = hh.get_vacancies_data()
    employers_data = hh.get_employers_data()

    truncate_tables(db_conn)
    insert_companies(db_conn, employers_data)
    insert_vacancies(db_conn, vacancies_data)

    dbmanager = DBManager(db_conn)
    filters = {
            1: ("Получает список всех работодателей и подсчитывает количество вакансий у каждого из них.", dbmanager.get_companies_and_vacancies_count),
            2: ("Собирает информацию обо всех вакансиях, включая название компании, название позиции, зарплату и ссылку на вакансию.", dbmanager.get_all_vacancies),
            3: ("Определяет среднюю зарплату среди всех вакансий.", dbmanager.get_avg_salary),
            4: ("Фильтрует вакансии, зарплата которых превышает среднюю зарплату по всему набору вакансий.", dbmanager.get_vacancies_with_higher_salary),
            5: ("Находит все вакансии, в названиях которых присутствуют определенные слова, указанные пользователем.", dbmanager.get_vacancies_with_keyword)
        }

    print('Доступные режимы вывода и фильтрации информации из базы данных')
    print()
    for key, (description, method) in filters.items():
        print(key, description)

    while True:
        user_input = input('Выберите номер фильтрации, который вас интересует: ')
        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            print("Завершение сеанса")
            break
        elif user_input in ['1', '2', '3', '4', '5']:
            if user_input == '5':
                keyword = input('Введите параметр поиска: ')
                method = filters[int(user_input)][1]
                result = method(keyword)
                for row in result:
                    print(*row)
                user_input_continue = input('Для продолжения нажмите любую клавишу или "exit" для выхода: ')
                if user_input_continue.lower() == 'exit':
                    break
            else:
                method = filters[int(user_input)][1]
                result = method()
                if isinstance(result, float):  # Проверяем, является ли результат числом с плавающей точкой
                    print(result)  # Просто печатаем результат, если это число
                else:
                    for row in result:
                        print(*row)  # Иначе итерируем по результату как обычно
                user_input_continue = input('Для продолжения нажмите любую клавишу или "exit" для выхода: ')
                if user_input_continue.lower() == 'exit':
                    break
        else:
            print('Пожалуйста, введите число от 1 до 5 или "exit" для выхода.')

    print("Конец работы функции")

if __name__ == '__main__':
    main()
