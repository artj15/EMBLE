# EMBLE APP

## Сборка приложения

docker-compose build

## Запуск БД и миграции

docker-compose up dbmate

## Запуск тестов

docker-compose run --rm emble_app pytest tests

## Запуск приложения

docker-compose up