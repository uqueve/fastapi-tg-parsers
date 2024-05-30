# Telegram News Parser

![Telegram Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/240px-Telegram_logo.svg.png)

## Описание

Этот проект представляет собой Backend для сайта + телеграмм бота для парсинга новостей с различных сайтов и отправки их в региональные каналы.

## Структура проекта

- **/api/backend**: Бэкенд на FastAPI для получения новостей.
- **/bot**: Работа с телеграмм ботом.
- **/database/mongo**: Работа с базой данных Mongo.
- **/docker_compose**: Докерфайлы и yaml-файлы.
- **/parsers**: Парсеры, модели и точка инициализации парсинга с постингом.
- **/traefik**: Докерфайл и yaml с настройкой проксирования и шифрования запросов.
- **/utils**: Сервисные функции, небольшие модули сторонних api, модели исключений.

## Установка и Запуск

Проект можно запустить в Docker контейнере. 
Запуск Traefik: 
```bash
docker compose -f traefik/docker-compose.traefik.yml up --build -d
```
Запуск MongoDB: 
```bash
make mongo
```
Запуск API: 
```bash
make app
```

## Конфигурация

Файл окружения должен быть заполнен в соответствии с .env.example.

## Лицензия

Этот проект лицензирован в соответствии с лицензией [MIT](LICENSE).
