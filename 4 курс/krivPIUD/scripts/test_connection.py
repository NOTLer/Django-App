"""Проверка полного цикла работы с PostgreSQL для лабораторной № 1."""

import os
import sys

from dotenv import load_dotenv
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()

REQUIRED_VARIABLES = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")
missing_variables = [name for name in REQUIRED_VARIABLES if not os.getenv(name)]

if missing_variables:
    print(
        "Не заданы переменные окружения: " + ", ".join(missing_variables) + ". "
        "Скопируйте .env.example в .env и повторите запуск.",
        file=sys.stderr,
    )
    raise SystemExit(1)

database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)

engine = create_engine(database_url, pool_pre_ping=True)
fake = Faker("ru_RU")
Faker.seed(42)

try:
    # engine.begin() сам фиксирует транзакцию при успешном завершении блока.
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS lab01_healthcheck (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(150) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT now()
                )
                """
            )
        )

        # Очистка делает проверку повторяемой: после каждого запуска будет 10 строк.
        connection.execute(text("TRUNCATE TABLE lab01_healthcheck RESTART IDENTITY"))

        rows = [
            {"full_name": fake.name(), "email": fake.unique.email()}
            for _ in range(10)
        ]
        connection.execute(
            text(
                """
                INSERT INTO lab01_healthcheck (full_name, email)
                VALUES (:full_name, :email)
                """
            ),
            rows,
        )

        row_count = connection.execute(
            text("SELECT count(*) FROM lab01_healthcheck")
        ).scalar_one()

    print(f"Строк в таблице lab01_healthcheck: {row_count}")
    print("Подключение, создание таблицы, запись и чтение из PostgreSQL работают.")
except (SQLAlchemyError, ValueError) as error:
    print(f"Не удалось выполнить проверку PostgreSQL: {error}", file=sys.stderr)
    raise SystemExit(1) from error
finally:
    engine.dispose()

