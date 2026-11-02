# Процессы и инструменты управления данными

Учебный проект с двумя первыми лабораторными работами курса. В первой
разворачивается окружение PostgreSQL, pgAdmin и Python, во второй подготовлена
модель управления данными для интернет-магазина «ШопЭксперт».

## Что находится в проекте

- `docker-compose.yml` — запуск PostgreSQL 16 и pgAdmin;
- `.env.example` — безопасный пример настроек подключения;
- `requirements.txt` — библиотеки Python;
- `scripts/test_connection.py` — проверка базы с созданием 10 тестовых строк;
- `docs/lab01_description.md` — простое подробное объяснение первой работы;
- `docs/lab02_governance_charter.md` — готовое задание второй работы;
- `docs/lab02_description.md` — простое подробное объяснение второй работы.

## Быстрый запуск лабораторной № 1

```bash
cp .env.example .env
docker compose up -d
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/test_connection.py
```

После запуска pgAdmin доступен по адресу <http://localhost:5050>. При добавлении
сервера внутри pgAdmin нужно указать host `postgres`, порт `5432`, имя базы,
пользователя и пароль из `.env`.

Для версий библиотек из методички лучше использовать Python 3.10–3.12. Проект
проверен на Python 3.11; более новый Python 3.14 может быть несовместим со
старыми закреплёнными версиями пакетов.

Остановить сервисы можно командой `docker compose down`. Данные PostgreSQL при
этом сохранятся в именованном томе `pg_data`.

