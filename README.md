![Python](https://img.shields.io/badge/python-3.11-blue)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-green)
![KivyMD](https://img.shields.io/badge/kivymd-1.2.0-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Release](https://img.shields.io/github/v/release/vitvikontYaPractic/workcalculator)

![Python](https://img.shields.io/badge/python-3.11-blue)
![Kivy](https://img.shields.io/badge/kivy-2.3.0-green)
![KivyMD](https://img.shields.io/badge/kivymd-1.2.0-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Release](https://img.shields.io/github/v/release/vitvikontYaPractic/workcalculator)

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
