# YaCut


### Описание
Сервис для создания коротких ссылок. Короткие ссылки ассоциируется с длинными
в базе данных и работают при помощи инструментов фреймворка. Можно создать короткую ссылку
самостоятельно или она будет сгенерирована автоматически при помощи рандомайзера.


### Технологии в проекте
    Flask 2.0.2, Jinja2 3.0.3, Sqlalchemy 1.4.29


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:MelodiousWarbler/yacut.git
```

```bash
cd yacut
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Создать в корневой папке файл .env с данными:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Создать базу данных и выполнить миграции:

```bash
flask db upgrade
```

Запустите проект:

```bash
flask run
```


### Автор:
- [Яков Плакотнюк](https://github.com/MelodiousWarbler "GitHub аккаунт")
