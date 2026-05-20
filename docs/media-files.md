# Медиафайлы — фото игроков, логотипы клубов

## Как хранятся

Django-Filer хранит медиафайлы в `./media/filer_public/<хэш>/<хэш>/<имя файла>`.

На сервере: bind-mount `./media → /app/media` общий для `web` и `nginx`.
Nginx отдаёт `/media/` напрямую из этой папки.

## Откуда берутся URL

`MEDIA_URL = '/media/'` → `obj.logo.url` возвращает `/media/filer_public/...` (путь).

Но если в `local_settings.py` настроен `FILER_STORAGES` с абсолютным URL
(например `http://dev.sportomatics.ru/media/`), то `.url` вернёт полный URL
с этим доменом. Это была причина ошибок Mixed Content.

**Исправление**: функции `_photo_path()` и `_url_path()` в сериализаторах
всегда обрезают схему+хост, возвращая только `/media/...`.

## Проверить медиафайлы на сервере

```bash
# Сколько файлов в медиа
find /opt/sportomatics/media -type f | wc -l

# Есть ли фото игроков (filer_public — django-filer)
ls /opt/sportomatics/media/filer_public/ | head

# Найти конкретный файл по имени
find /opt/sportomatics/media -name "lokomotiv.gif"
```

## Если файлы отсутствуют

Медиафайлы **не хранятся в git** и **не восстанавливаются при деплое**.
Они должны быть скопированы вручную из бэкапа или с другого сервера.

```bash
# Скопировать медиафайлы с другого сервера
rsync -av user@old-server:/path/to/media/ /opt/sportomatics/media/

# Или восстановить из архива
tar -xzf media-backup.tar.gz -C /opt/sportomatics/media/
```

После копирования файлов перезапуск не нужен — nginx отдаёт их сразу.

## Загрузка медиафайлов через Admin

Фото игроков и логотипы можно загружать через Django Admin → Filer:
`https://khl.sportomatics.com/admin/filer/`

При загрузке файл попадает в `./media/filer_public/` автоматически.

## 404 на логотипы клубов

Причина: файлы `.gif`/`.jpg` из базы данных не существуют в `./media/`.
Код работает корректно — URL генерируется правильно, но файла нет.

Решение: скопировать медиафайлы из бэкапа.
