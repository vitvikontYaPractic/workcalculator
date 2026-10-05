# Архитектура Work Calculator

Документ описывает структуру проекта, потоки данных и зависимости.

## Общая схема

    ┌─────────────────────────────────────────────────┐
    │           Android (arm64-v8a / armeabi-v7a)     │
    │                                                 │
    │  ┌───────────────────────────────────────────┐  │
    │  │           WorkCalculatorApp               │  │
    │  │           (main.py, MDApp)                │  │
    │  │  - title = "Work Calculator"              │  │
    │  │  - theme_cls.primary_palette = "Green"    │  │
    │  │  - build() -> Box()                       │  │
    │  └────────────────┬──────────────────────────┘  │
    │                   │                             │
    │                   ▼                             │
    │  ┌───────────────────────────────────────────┐  │
    │  │              Box (MDBoxLayout)            │  │
    │  │              loading.py                   │  │
    │  │  - UI-логика + расчёты                    │  │
    │  │  - 14 ObjectProperty (привязки к .kv)     │  │
    │  └────┬─────────────────────────────┬────────┘  │
    │       │                             │           │
    │       ▼                             ▼           │
    │  ┌──────────────┐            ┌──────────────┐   │
    │  │ workcalculator│            │  database/   │   │
    │  │     .kv       │            │  models.py   │   │
    │  │ (UI-разметка) │            │ (Product)    │   │
    │  └──────────────┘            └──────┬───────┘   │
    │                                     │           │
    │                                     ▼           │
    │                              ┌──────────────┐   │
    │                              │   date.db    │   │
    │                              │   (SQLite)   │   │
    │                              └──────────────┘   │
    │                                                 │
    │  ┌───────────────────────────────────────────┐  │
    │  │           logs/debug_log.py               │  │
    │  │           (loguru logger)                 │  │
    │  └───────────────────────────────────────────┘  │
    └─────────────────────────────────────────────────┘

## Модули

### main.py — точка входа

    from kivymd.app import MDApp
    from kivymd.theming import ThemeManager
    from loading import Box
    from database.models import db, Product

    class WorkCalculatorApp(MDApp):
        title = 'Work Calculator'

        def build(self):
            self.theme_cls = ThemeManager()
            self.theme_cls.primary_palette = "Green"
            self.theme_cls.primary_hue = "600"
            db.connect()
            db.create_tables([Product])
            db.close()
            return Box()

### loading.py — логика и UI

Класс `Box(MDBoxLayout)` — центральный элемент. Содержит:

**ObjectProperty (привязки к виджетам в .kv):**
- `drop_btn` -> `speed_dial` (Speed dial меню)
- `menu_bt` -> `button_menu` (кнопка выбора изделия)
- `label_product` -> `name_product` (название изделия)
- `enter_text` -> `text_input` (поле ввода)
- `label_widget1` -> `label_numer` (номер изделия)
- `label_widget2` -> `label_Pn` (периметр начальный)
- `label_widget3` -> `label_Pc` (периметр конечный)
- `label_widget4` -> `label_Dn` (диаметр начальный)
- `label_widget5` -> `label_Dc` (диаметр конечный)
- `label_widget6` -> `label_height` (глубина среза)
- `label_widget7` -> `label_length` (длина обработки)
- `table` -> `data_table` (ScrollView с таблицей)
- `widget_search` -> `search_input` (поле поиска)

**Методы:**

| Метод | Назначение |
|---|---|
| `bar_menu` | Меню в TopAppBar (Допуски, О программе) |
| `menu_bar_callback` | Обработка выбора в меню |
| `delete_row` | Удаление выделенных записей (галочки) |
| `clear_database` | Очистка всей БД с диалогом |
| `search_base` | Поиск по номеру |
| `tables_data` | Показать все записи (журнал) |
| `show_dialog` | Предпросмотр данных |
| `close_dialog` | Закрытие диалога |
| `get_info` | Сбор данных для предпросмотра |
| `backspace` | Очистка поля ввода |
| `drop_menu` | Меню выбора изделия |
| `menu_callback` | Выбор изделия |
| `numer_product` | Номер изделия |
| `text_Pn` | Периметр начальный |
| `text_Pc` | Периметр конечный |
| `text_Dn` | Расчёт начального диаметра (Pn / pi) |
| `text_Dc` | Расчёт конечного диаметра (Pc / pi) |
| `text_height` | Расчёт глубины среза ((Dn - Dc) / 2) |
| `length` | Длина обработки |
| `clear_text` | Обнуление полей |
| `save_create_tables` | Сохранение в БД |
| `closed` | Закрытие приложения |

### workcalculator.kv — UI-разметка

Разметка на языке Kivy. Ключевые элементы:

- `<Box>` — корневой класс.
- `MDTopAppBar` — верхняя панель "Калькулятор токаря".
- `MDBottomNavigation` — нижняя навигация с 2 экранами:
  - **Screen 1** — "Калькулятор":
    - `text_input` (поле ввода)
    - `MDGridLayout` с 8 строками кнопок + значений
    - `speed_dial` (FloatingActionButtonSpeedDial)
  - **Screen 2** — "Журнал / Поиск":
    - `search_input` (поле поиска)
    - `data_table` (ScrollView)
    - Кнопки: Журнал / Поиск / Удалить / Очистить

### database/models.py — модель БД

    from peewee import *

    db = SqliteDatabase('database/date.db')

    class BaseModel(Model):
        class Meta:
            database = db

    class Product(BaseModel):
        class Meta:
            db_table = "Products"

        brigade = CharField(max_length=10)
        number = CharField(max_length=10)
        product = CharField(max_length=10)
        diameter_first = CharField(max_length=10)
        diameter_last = CharField(max_length=10)
        height = CharField(max_length=10)
        length = CharField(max_length=10)
        created = DateTimeField(
            constraints=[SQL("DEFAULT (datetime('now'))")])

### logs/debug_log.py — логирование

    from loguru import logger

    logger.add(
        "logs/debug.json",
        format="{time}{level}{message}",
        level="DEBUG",
        rotation="400 KB",
        compression="zip",
        serialize=True
    )

Используется через декоратор `@logger.catch` на методах `Box`.

## Потоки данных

### Сохранение записи

    Пользователь
        |
        v
    [text_input]  -- ввод номера
        |
        v
    [numer_product]  -- нажатие кнопки
        |
        v
    [label_widget1]  -- отображение
        |
        v
    [save_create_tables]  -- нажатие "Сохранить"
        |
        v
    Product(...).save()  -- peewee INSERT
        |
        v
    [date.db]  -- SQLite

### Поиск

    Пользователь
        |
        v
    [search_input]  -- ввод номера
        |
        v
    [search_base]  -- нажатие "Поиск"
        |
        v
    Product.select().where(Product.number == self.numb)
        |
        v
    MDDataTable с row_data
        |
        v
    [data_table]

### Удаление по галочкам

    Пользователь ставит галочки в MDDataTable
        |
        v
    [delete_row]
        |
        v
    data_table.get_row_checks()  -- список выделенных строк
        |
        v
    Product.delete().where(Product.number == row[0])
        |
        v
    tables_data()  -- обновление таблицы

### Очистка БД

    Пользователь нажимает "Очистить"
        |
        v
    [clear_database] -- открывает MDDialog
        |
        v
    Подтверждение
        |
        v
    [_confirm_clear_database]
        |
        v
    Product.delete().execute()  -- удалить все
        |
        v
    tables_data() -- пустая таблица

## Зависимости

### Runtime (Python-пакеты в APK)

| Пакет | Версия | Назначение |
|---|---|---|
| kivy | 2.3.0 | UI-фреймворк |
| kivymd | 1.2.0 | Material Design виджеты |
| materialyoucolor | 2.0.9 | Material You палитра |
| asynckivy | 0.6.2 | Асинхронность для KivyMD |
| peewee | 3.17.1 | ORM для SQLite |
| loguru | 0.7.2 | Логирование |
| pillow | 10.3.0 | Работа с изображениями |

### Build-time (p4a recipes)

| Recipe | Назначение |
|---|---|
| python3 | Python 3.11.13 для Android |
| hostpython3 | Python для сборки (x86_64) |
| kivy | Kivy 2.3.0 |
| kivymd | KivyMD 1.2.0 |
| materialyoucolor | Material You |
| pyjnius | Python <-> Java мост |
| pillow | Pillow для KivyMD |
| freetype, harfbuzz | Шрифты |
| png, jpeg, libwebp | Изображения |
| openssl, sqlite3, libffi | Системные |
| sdl2, sdl2_image, sdl2_mixer, sdl2_ttf | Мультимедиа |

## Сборка APK

См. BUILD_NOTES.md — детальные патчи p4a.

**Ключевые модификации p4a:**

1. **Python 3.11** вместо 3.14 (Kivy 2.3.0 несовместим с 3.14).
2. **Cython 3.0.12** — компромисс между Kivy (<=3.0.0) и pyjnius (~=3.1.2).
3. **`--no-isolation`** для `-m build` (иначе теряется PYTHONPATH).
4. **`PKG_CONFIG_LIBDIR=/dev/null`** — блокирует хост-заголовки (/usr/include).
5. **Удаление `/usr/include` из CFLAGS** — иначе `__GNUC_PREREQ` ошибка.
6. **`prebuild_arch`** — патчит `pyproject.toml` у Kivy и pyjnius.
7. **`--without-brotli`** для freetype (NDK 25b не имеет brotli).

## Структура каталогов

    WorkCalculatorFinal/
    |-- main.py                # MDApp точка входа
    |-- loading.py             # Box (UI + логика)
    |-- workcalculator.kv      # Kivy UI разметка
    |-- database/
    |   |-- models.py          # Product (peewee)
    |   |-- date.db            # SQLite (НЕ в git)
    |   `-- __init__.py
    |-- logs/
    |   |-- debug_log.py       # loguru конфиг
    |   |-- debug.json         # Логи (НЕ в git)
    |   `-- __init__.py
    |-- icons/
    |   `-- icon.png           # 512x512, APK иконка
    |-- buildozer.spec         # Конфиг сборки
    |-- requirements.txt       # Версии пакетов
    |-- README.md              # Описание проекта
    |-- ARCHITECTURE.md        # Этот файл
    |-- BUILD_NOTES.md         # Патчи p4a
    `-- LICENSE                # MIT

## Жизненный цикл приложения

1. **Запуск** -> `main.py` -> `WorkCalculatorApp.build()`.
2. **Инициализация БД** -> `db.connect()` + `db.create_tables([Product])`.
3. **Возврат Box()** -> Kivy строит UI из `workcalculator.kv`.
4. **Пользователь работает** -> методы Box -> сохранение в БД.
5. **Закрытие** -> `closed()` -> `quit()`.

## Особенности Android-версии

- **Приватное хранилище:** `/data/data/org.workcalculator/files/`.
- **Ориентация:** портретная (`orientation = portrait`).
- **Fullscreen:** да (`fullscreen = 1`).
- **Мин. API:** 21 (Android 5.0).
- **Разрешения:** INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE.
