import psycopg2


class DBConnection:
    """
    Класс для подключения к базе данных с заданными параметрами
    """

    def __init__(self, name, params):
        self.params = params
        self.conn = psycopg2.connect(database=name, **self.params)

    def conn_close(self):
        self.conn.close()


def create_tables(db_conn):
    """
    Создает таблицы для хранения данных о компаниях и вакансиях в базе данных.
    """
    with db_conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL
                );
            """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255) NOT NULL,
                company_id INT NOT NULL REFERENCES companies(id),
                salary_min INT,
                salary_max INT
            );
        """)
        db_conn.commit()


def insert_vacancies(db_conn, vacancies_data):
    """
    Сохраняет данные о вакансиях в базе данных.
    """
    with db_conn.cursor() as cursor:
        for vacancy in vacancies_data:
            cursor.execute(
                """
                INSERT INTO vacancies(id, name, url, company_id, salary_min, salary_max)
                VALUES (%s,%s,%s,%s,%s,%s);
                """, (
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['url'],
                    vacancy['employer']['id'],
                    vacancy['salary']['from'],
                    vacancy['salary']['to']
                )
            )
            db_conn.commit()


def insert_companies(db_conn, employers_data):
    """
    Сохраняет данные о компаниях в базе данных.
    """
    with db_conn.cursor() as cursor:
        for employer in employers_data:
            cursor.execute(
                """
                INSERT INTO companies(id, name, url)
                VALUES (%s,%s,%s);
                """, (
                    employer['id'],
                    employer['name'],
                    employer['url']
                )
            )
            db_conn.commit()


def truncate_tables(db_conn):
    """
    Удаление всех записей из таблиц
    """
    with db_conn.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE companies RESTART IDENTITY CASCADE;
            """
        )
        cursor.execute(
            """
            TRUNCATE TABLE vacancies RESTART IDENTITY;
            """
        )
        db_conn.commit()
