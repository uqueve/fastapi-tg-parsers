```markdown
# Telegram News Parser

![Telegram Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/240px-Telegram_logo.svg.png)

## Описание

Этот проект представляет собой телеграмм бота для парсинга новостей с различных сайтов и отправки их в чат.

## Структура проекта

- **/handlers**: Роутеры телеграмм бота.
- **/database**: Скрипты для работы с базой данных.
- **/parsers**: Скрипты парсинга сайтов.
- **/utils**: Сервисные функции.

## Установка и Запуск

Проект можно запустить в Docker контейнере.

### Зависимости

Перед запуском убедитесь, что у вас установлен Docker.

### Установка

Сборка Docker образа:

```bash
docker build -t cyprusnews /root/cyprusnews
```

### Запуск

Запустите Docker контейнер:

```bash
docker run --restart always --name cyprusnews_container -d -v /root/cyprusnews:/cyprusnews cyprusnews
```

## Конфигурация

Файл окружения расположен в корневой директории проекта.

Файл для работы с базой данных: `telegram-news-parser/database/db.py`.

Конфигурация: `telegram-news-parser/config_data/config.py`.

Прокси находятся в файле: `telegram-news-parser/parsers/base_parser.py`.

## Лицензия

Этот проект лицензирован в соответствии с лицензией [MIT](LICENSE).
```
