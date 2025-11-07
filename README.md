# TradeFlow Journal — Starter


Это минимальная, но полная версия backend для TradeFlow Journal.


## Что внутри
- FastAPI приложение с регистрацией/входом (JWT)
- Роли: `user` и `admin`
- Таблицы: users, accounts, trades
- Endpoint `/import_mt5` для приёма сделок (авторизованный)
- Пример `mt5_uploader.py` для запуска на машине с MT5


## Быстрая инструкция по развёртыванию (Render)
1. Создай репозиторий `tradeflow-journal` и запушь файлы.
2. На Render: Create -> Web Service -> Connect GitHub -> выбери репо.
3. В Render укажи Docker build и добавь переменные окружения (см `.env.example`).
4. Добавь PostgreSQL (Render Databases) и заполни `DATABASE_URL` к нему.
5. Разверни и перейди по ссылке — приложение будет доступно.


## Локальный запуск (для тестов)
1. Установи зависимости: `pip install -r requirements.txt`.
2. Создай локальный PostgreSQL или запусти через Docker.
3. Экспортируй переменные окружения (см `.env.example`).
4. Запусти `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
5. Создай таблицы: запусти Python и выполните `from app.models import Base, engine; Base.metadata.create_all(bind=engine)`.


## Как подключить MT5
1. На машине с MT5 установи терминал и убедись, что MT5 открыт.
2. Заполни `mt5_uploader.py` переменными: `MT5_ACCOUNT_LOGIN`, `API_URL`, `API_TOKEN`.
3. Запусти `python mt5_uploader.py` — он выгрузит сделки и отправит в `/import_mt5`.
