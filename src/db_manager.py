import decimal


class DBManager:
    """
    Класс управления базами данных PostgreSQL для взаимодействия с ней.
    """

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def get_avg_salary(self):
        """
        Определяет среднюю зарплату среди всех вакансий.
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT AVG(salary_min) FROM vacancies;
                """
            )
            result = cursor.fetchone()[0]
            if isinstance(result, decimal.Decimal):
                return float(round(result))
            else:
                return result

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех работодателей и подсчитывает количество вакансий у каждого из них.
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT companies.name, COUNT(vacancies.id) AS vacancy_count
                FROM companies
                LEFT JOIN vacancies ON companies.id = vacancies.company_id
                GROUP BY companies.name;
            """)
            companies_vacancies_count = cursor.fetchall()
            return companies_vacancies_count

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT companies.name AS company_name, vacancies.name AS vacancy_name,
                       vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                INNER JOIN companies ON vacancies.company_id = companies.id;
            """)
            all_vacancies = cursor.fetchall()
            return all_vacancies

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT companies.name AS company_name, vacancies.name AS vacancy_name, vacancies.salary_min, vacancies.salary_max, vacancies.url 
                FROM vacancies
                INNER JOIN companies ON vacancies.company_id = companies.id
                WHERE (vacancies.salary_min) > (SELECT AVG(salary_min) FROM vacancies);
            """)
            high_salary_vacancies = cursor.fetchall()
            return high_salary_vacancies

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        with self.db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT companies.name AS company_name, vacancies.name AS vacancy_name,
                       vacancies.salary_min, vacancies.salary_max, vacancies.url
                FROM vacancies
                INNER JOIN companies ON vacancies.company_id = companies.id
                WHERE LOWER(vacancies.name) LIKE %s;
            """, ('%' + keyword.lower() + '%',))
            keyword_vacancies = cursor.fetchall()
            return keyword_vacancies
