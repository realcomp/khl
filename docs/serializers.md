# Сериализаторы — устройство и правила

## Иерархия сериализаторов

### Базовые (api/base/serializers.py)

- `LangDepSerializer` — добавляет `_get_field()` для локализованных полей
- `TitleBaseSerializer` — добавляет `title` через `_get_field`
- `FIFSerialiser` — для django-filer `Image`, возвращает `{id, file, name, _height, _width}`
- `SeasonSerializer`
- `_url_path(url)` — утилита: обрезает схему+хост из URL

### Основные (hockeyapp/serializers/__init__.py)

- `AbstractManSerializer` — `fio`, `name`, `lastname` через локаль
- `BaseClubSerializer` — `{id, title, logo, url}`
- `ClubLightListSerializer` — `BaseClub` + `title_verbose`, `address`
- `ClubListSerializer` — полный список клубов
- `PlayerCardSerializer` — карточка игрока (главная страница игрока)
- `MetricsPlayerSerializer` — для метрик/сравнения
- `_photo_path(photo_field)` — утилита: `photo_field.url` → обрезает схему+хост

### Сериализаторы клубов (hockeyapp/serializers/clubs.py)

- `ClubTeamPlayerSerializer` — игроки в составе команды
- `ScheduleClubSerializer` — клуб в расписании матчей
- `ClubMainAboutSerializer` — полная информация о клубе
- `OriginPlayersSerilizer` — игроки с историей
- `ClubCoachesSerilizer` — тренеры

### API сериализаторы (api/hockey/serializers.py)

- `ClubListSerializer` — список клубов для API
- `PartnerPlayerSerializer` — партнёры игрока (использует `FIFSerialiser` для фото!)
- `PlayerMinimalSerialiser` — базовый сериализатор игрока для API

## Правило для фото и логотипов

**Никогда не использовать `ReadOnlyField(source='photo.url')` или `ReadOnlyField(source='logo.url')`** — они вернут полный URL с неправильным доменом.

**Всегда использовать SerializerMethodField:**

```python
# В hockeyapp/serializers/
from . import _photo_path

photo = serializers.SerializerMethodField()
def get_photo(self, obj):
    return _photo_path(obj.photo)

logo = serializers.SerializerMethodField()
def get_logo(self, obj):
    return _photo_path(obj.logo)
```

```python
# В api/base/serializers.py или api/hockey/serializers.py
from api.base.serializers import _url_path

logo = drf.serializers.SerializerMethodField()
def get_logo(self, obj):
    return _url_path(obj.logo.url if obj.logo else None)
```

## FIFSerialiser — особый случай

`FIFSerialiser` возвращает **объект**, а не строку:

```json
{"id": 1686, "file": "/media/filer_public/29/85/.../3892.jpeg", "name": "3892.JPEG", "_height": 221, "_width": 165}
```

В Angular-шаблонах использовать только **`.file`** для получения URL:

```html
<!-- ПРАВИЛЬНО -->
<img ng-src="{{player.photo.file}}">

<!-- НЕПРАВИЛЬНО — вставит весь JSON-объект как URL -->
<img ng-src="{{player.photo}}">
```

`FIFSerialiser` используется в:
- `PlayerMinimalSerialiser` (api/hockey/serializers.py) → партнёры, поиск игроков
- `IIFMinimalSerializer` (api/base/serializers.py) → инстаграм-фото арен

## Локализация полей

Модели с `get_locale_attr()` поддерживают `ru_title` / `en_title`, `ru_fio` / `en_fio` и т.д.

`LangDepSerializer._get_field(obj, 'title')` возвращает нужную локаль из `request`.

При сериализации передавать `context={'request': request}`:
```python
ClubListSerializer(queryset, many=True, context={'request': request})
```

Без `request` в контексте — всегда вернёт дефолтное (обычно русское) поле.
