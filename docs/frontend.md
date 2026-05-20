# Фронтенд — AngularJS, шаблоны, JS

## Структура JS

```
base/static/js/
  controllers/    — AngularJS-контроллеры (*.js + *.coffee исходники)
  services/       — AngularJS-сервисы
  libs/           — сторонние библиотеки
  router.js       — маршрутизация Angular
  script.min.js   — общий скрипт

base/static/build/
  app.js          — собранный бандл всех контроллеров и сервисов
  libs.min.js     — сторонние библиотеки (jquery, angular, semantic, etc.)
```

## app.js — сборка

`app.js` = конкатенация всех файлов из `base/static/js/` через Gulp 3.

**Gulp 3 не работает на Node 20+** (`primordials` error). Не использовать `gulp`.

Для ручной пересборки — см. [legacy-issues.md](legacy-issues.md#gulp-3--нерабочий).

После изменения любого JS-контроллера или сервиса:
1. Пересобрать `app.js` вручную
2. Закоммитить `base/static/build/app.js`
3. Задеплоить (`docker compose build web` + `docker compose up -d web`)
4. Статика обновится через `collectstatic` в entrypoint

## Шаблоны Django + AngularJS

Django-шаблоны используют `{{ }}` для своих переменных, Angular тоже.
Чтобы они не конфликтовали, Angular-блоки оборачиваются в `{% verbatim %}`:

```html
{% verbatim %}
<div ng-repeat="player in players">
    <img ng-src="{{player.photo.file}}">
    <p>{{player.fio}}</p>
</div>
{% endverbatim %}
```

Переменные **вне** `{% verbatim %}` — Django-контекст (рендерится на сервере):
```html
<img src="{{ photo }}">  {# photo — из Django context #}
```

## ng-src vs src

Браузер немедленно загружает `src="..."` — **до** того как Angular успеет заменить
`{{player.photo.file}}` на реальный URL. В результате делается запрос на буквальный
URL `{{player.photo.file}}` (404).

**Правило**: для динамических Angular-значений всегда `ng-src`, никогда `src`:

```html
<!-- ПРАВИЛЬНО -->
<img ng-src="{{player.photo.file}}">
<img ng-src="{{club.logo || ''}}">

<!-- НЕПРАВИЛЬНО — браузер запросит буквально "{{player.photo.file}}" -->
<img src="{{player.photo.file}}">
```

## Основные контроллеры

| Контроллер | Страница | API |
|---|---|---|
| `PlayerPartnersController` | Партнёры игрока | `api:hockey:player_partners` |
| `PlayerCardIndicatorsController` | Карточка игрока (графики) | `hockeyapp:player-card-indicators-api` |
| `ClubTeamController` | Состав команды | `hockeyapp:club-team-api` |
| `ClubListController` | Список клубов | `api:hockey:club-list-api` |
| `ClubTeamCompareController` | Сравнение команд | — |
| `ClubStatsController` | Статистика клуба | — |
| `PlayersSearchController` | Поиск игроков | — |
| `MetricsPlayersController` | Метрики игроков | — |

## Ключевые hidden input для Angular

Angular-контроллеры получают API URL через скрытые `<input>` поля в шаблоне:

```html
<input id="club-team-api" type="hidden" value="{% url 'hockeyapp:club-team-api' pk %}">
<input id="api-player-indicators" type="hidden" value="{% url 'hockeyapp:player-card-indicators-api' pk %}">
<input id="api-player-partners" value="{% url 'api:hockey:player_partners' pk %}">
```

В JS читается через `$('#club-team-api').val()`.

## Библиотеки фронтенда

- AngularJS ~1.x
- jQuery 2.x (через `libs.min.js`)
- Semantic UI (CSS фреймворк)
- Highcharts / Highstock (графики)
- AmCharts (графики)
- Leaflet (карты)
- isteven-multi-select (мультиселект)
- angucomplete (автокомплит)
- ionrangeslider (слайдеры)
- underscore.js (`_` доступен глобально)

## Bower

Сторонние компоненты установлены через Bower в `bower_components/`.
В продакшн через Django-приложение `bower` (mounted в статику).
Обновлять через `bower install` — но это устаревший инструмент.

## Мобильные шаблоны

Некоторые секции имеют отдельную мобильную навигацию через `mlpushmenu.html`:
```html
{% include "hockeyapp/clubs/mlpushmenu.html" with section="club" active_section="club-stats" active_menu="stats-compare" %}
```

Это side-drawer меню для xs-экранов.
