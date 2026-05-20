# Деплой на сервер

## Где всё находится

- **Сервер**: `/opt/sportomatics/` (пользователь `root`)
- **Git remote**: `git@github.com:realcomp/khl.git`
- **Рабочая ветка**: `perf-audit-autofix` (или `main` — смотреть по контексту)

## Критически важно: код запечён в Docker-образ

`COPY . /app/` в Dockerfile означает что **весь Python-код и шаблоны** попадают в образ при `docker compose build`.

`git pull` + `docker compose restart web` **НЕ обновляет** Python-код и Django-шаблоны в контейнере — контейнер продолжает работать на старом образе.

## Стандартный деплой (Python/шаблоны/JS изменились)

```bash
# На сервере в /opt/sportomatics/

# 1. Получить новый код
git pull origin <ветка>

# 2. Пересобрать образ с новым кодом
docker compose build web

# 3. Запустить с новым образом
docker compose up -d web

# 4. Статика (app.js и всё остальное) обновится автоматически
#    через collectstatic в docker-entrypoint.sh
#    Если нужно вручную:
docker compose exec web python manage.py collectstatic --noinput
```

## Деплой только nginx-конфига или статики

```bash
# Если изменился только nginx/default.conf
docker compose restart nginx

# Если нужно принудительно обновить статику в nginx-томе
docker compose exec web python manage.py collectstatic --noinput
docker compose restart nginx
```

## Деплой только медиафайлов (фото, логотипы)

Медиафайлы монтируются как bind-mount `./media:/app/media` —
копировать прямо в `/opt/sportomatics/media/filer_public/...`

```bash
# Скопировать с другого сервера или из бэкапа
rsync -av /source/media/ root@server:/opt/sportomatics/media/
```

## Посмотреть логи

```bash
docker compose logs web --tail=50
docker compose logs nginx --tail=20
docker compose logs celery_worker --tail=30
```

## Перезапустить всё

```bash
docker compose down && docker compose up -d
```

## Проверить что запущено

```bash
docker compose ps
```

## Workflow разработки

1. Редактируем код локально (Mac, `/Users/Shared/Projects/khl/`)
2. Коммитим через VSCode Git
3. `git push origin <ветка>` (или через интерфейс VSCode)
4. На сервере: `git pull` + `docker compose build web` + `docker compose up -d web`

> **Нет локального Docker** — все проверки делаются напрямую на сервере.
> Не тратить время на попытки запустить проект локально.
