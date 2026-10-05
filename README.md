# Work Calculator (Калькулятор токаря)

Android-приложение для токарных расчётов. Восстановлено из утерянного проекта в октябре 2026.

## Функции

- Расчёт параметров обработки: начальный/конечный диаметр, глубина среза, длина
- База данных SQLite для хранения записей
- Журнал с таблицей всех записей
- Поиск по номеру изделия
- Удаление по галочкам
- Очистка всей БД с подтверждением
- Выбор изделия из списка
- Material You тема

## Установка

Скачать APK из раздела Releases и установить на Android 5+.

## Сборка

См. BUILD_NOTES.md.

    cd ~/Projects/WorkCalculatorFinal
    source .venv/bin/activate
    export PIP_BREAK_SYSTEM_PACKAGES=1
    buildozer -v android debug

## Технологии

- Kivy 2.3.0 + KivyMD 1.2.0
- materialyoucolor 2.0.9
- peewee 3.17.1
- loguru 0.7.2
- Buildozer + python-for-android

## Лицензия

MIT
