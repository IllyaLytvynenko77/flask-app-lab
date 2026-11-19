# Лабораторна робота №4 — Flask (Blueprints, request, сесії та cookie)

Проєкт реструктуризовано за архітектурою лабораторної роботи №3 (Application Factory + Blueprints).

## Структура проєкту

```text
flask_lab4_blueprints/
├── app/
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   ├── users/
│   │   │   ├── login.html
│   │   │   └── profile.html
│   │   └── base.html
│   ├── users/
│   │   ├── __init__.py
│   │   └── views.py
│   ├── __init__.py
│   └── views.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── .flaskenv
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Запуск (Windows)

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
flask run
```
Або через `run.py`:
```bash
py run.py
```

Відкрийте у браузері: `http://127.0.0.1:5000`

- **Логін:** `admin`
- **Пароль:** `12345`

## Запуск тестів

```bash
py -m unittest discover tests
```
