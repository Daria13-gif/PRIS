# Авторы

- Полякова Дарья К3342
- Жижилева Арина К3342


# Лабораторная работа №2: Разработка микросервисной архитектуры с GraphQL

## Описание

Учебный проект, демонстрирующий микросервисную архитектуру с использованием GraphQL и Apollo Gateway.  
Приложение состоит из трёх микросервисов: Пользователи, Товары и Заказы. Все взаимодействия происходят через GraphQL API.

## Как запустить

1. Убедитесь, что установлены:

- Python 3.10+
- PostgreSQL
- MongoDB
- Node.js + npm

2. Создайте базы данных:

- `users_db` (PostgreSQL)
- `products_db` (PostgreSQL)
- `orders_db` создастся автоматически в MongoDB при первом запросе

3. Установите зависимости Python для каждого микросервиса:
```
pip install fastapi uvicorn strawberry-graphql[fastapi] sqlalchemy psycopg2 pymongo motor
```
4. Установите зависимости Node.js в папке gateway:
```
cd gateway
npm install
```
5. Запустите микросервисы (в отдельных терминалах):
```
cd users_service
uvicorn main:app --port 8001

cd products_service
uvicorn main:app --port 8002

cd orders_service
uvicorn main:app --port 8003
```
6. Запустите GraphQL Gateway:
```
cd gateway
node index.js
```
7. Откройте браузер:
```
http://localhost:4000
```

## Функциональность

- Получение списка пользователей, товаров и заказов
- Создание новых пользователей, товаров и заказов
- Обновление записей (пользователей, товаров, заказов)
- Удаление записей
- Объединение всех микросервисов в один GraphQL API через Apollo Gateway

## Используемые библиотеки

Python микросервисы:
- FastAPI
- Strawberry GraphQL
- SQLAlchemy
- psycopg2
- Motor (для MongoDB)

GraphQL Gateway:
- Apollo Server
- Apollo Gateway
- GraphQL (Node.js)

# Лабораторная работа №3: Работа с Big Data

## Описание

Веб-приложение на Flask, позволяющее загружать большие данные (CSV), обучать простую ML-модель и визуализировать результаты.

## Как запустить

1. Клонируй репозиторий:
```
git clone https://github.com/ИМЯ_ПОЛЬЗОВАТЕЛЯ/big-data-lab.git
cd big-data-lab
```
2. Установи зависимости:
```
pip install -r requirements.txt
```
3. Запусти Flask-приложение:
```
python app.py
```
4. Перейди в браузер:
```
http://127.0.0.1:5000/
```

## Функциональность

- Загрузка CSV-файлов
- Предпросмотр таблицы
- Выбор признаков X и Y
- Обучение модели (линейная регрессия)
- Построение графиков
- Корреляционная матрица

## Используемые библиотеки

- Flask
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn

