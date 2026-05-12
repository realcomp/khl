#!/bin/bash

# Этот скрипт подготавливает директорию для запуска Docker Compose
# Предполагается, что скрипт запускается из корня проекта: spool/app/sportomatics

echo "Создание директорий..."
mkdir -p ./docker-entrypoint-initdb.d
mkdir -p ./media
mkdir -p ./nginx

# Копирование дампа базы данных из текущей папки
DB_DUMP="./sportomatics_20160705.sql.gz"
if [ -f "$DB_DUMP" ]; then
    echo "Копирование дампа БД $DB_DUMP..."
    cp "$DB_DUMP" ./docker-entrypoint-initdb.d/
else
    echo "Дамп БД $DB_DUMP не найден. Пропустите этот шаг, если у вас чистая БД."
fi

# Распаковка медиа-файлов
MEDIA_ARCHIVE="./media.tar.bz2"
if [ -f "$MEDIA_ARCHIVE" ]; then
    echo "Распаковка $MEDIA_ARCHIVE в папку ./media..."
    tar -xjf "$MEDIA_ARCHIVE" -C ./media --strip-components=1
else
    echo "Архив с медиа $MEDIA_ARCHIVE не найден."
fi

# Сборка и запуск
echo "Готово! Теперь вы можете запустить проект:"
echo "docker-compose build"
echo "docker-compose up -d"
