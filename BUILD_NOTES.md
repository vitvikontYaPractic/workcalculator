# Work Calculator — Заметки по сборке APK

**Успешная сборка:** 5 октября 2026, версия 0.0.38
**APK:** bin/workcalculatorapp-0.0.38-arm64-v8a_armeabi-v7a-debug.apk (54 МБ)

## Окружение
- Python 3.12 (системный, /usr/bin/python3)
- Buildozer 1.5.1.dev0
- p4a: коммит 6b66944a (Python 3.11.13), ветка py311
- Android SDK: ~/Android/Sdk
- Android NDK: 25.1.8937393 (25b)
- Java: OpenJDK 17

## Ключевые параметры buildozer.spec
- icon.filename = %(source.dir)s/icons/icon.png
- requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor==2.0.9,asynckivy==0.6.2,loguru==0.7.2,peewee==3.17.1,pillow==10.3.0,...
- android.archs = arm64-v8a, armeabi-v7a
- p4a.url = file:///tmp/p4a-mirror
- p4a.branch = py311

## Локальное зеркало p4a
p4a develop использует Python 3.14 — несовместим с Kivy 2.3.0.
Нужен коммит 6b66944a (Python 3.11.13) как ветка py311 в /tmp/p4a-mirror.

## Патчи в p4a recipe.py
1. Recipe.get_recipe_env — убрать -I/usr/include из CFLAGS/CPPFLAGS
2. PyProjectRecipe.get_recipe_env — PYTHONPATH + убрать -I/usr/include
3. PyProjectRecipe.build_arch — --no-isolation в build_args
4. install_hostpython_prerequisites — фильтр cython

## Патчи в Kivy recipe
1. hostpython_prerequisites = [] (убрать Cython)
2. prebuild_arch — заменить cython<=3.0.0 → cython
3. get_recipe_env — PKG_CONFIG_LIBDIR=/dev/null

## Патчи в pyjnius recipe
1. prebuild_arch — заменить Cython~=3.1.2 → Cython

## Патчи в freetype recipe
1. --without-brotli в config_args

## Ручные правки hostpython3
Путь: .buildozer/.../other_builds/hostpython3/desktop/hostpython3/
1. Симлинк python3 → native-build/python
2. Симлинк lib → Lib
3. Симлинк build → native-build/build
4. Скопированы *.so из native-build/build/lib.linux-x86_64-3.11/ в Lib/lib-dynload/
5. Скопированы setuptools/pip/build/Cython в Lib/site-packages/
6. Удалён setuptools-65.5.0.dist-info
7. Установлены setuptools>=77, Cython==3.0.12, wheel

## Cython версии
- Kivy 2.3.0 требует cython<=3.0.0
- pyjnius 1.7.0 требует Cython~=3.1.2
- Установлен Cython 3.0.12 (компромисс, оба собираются)

## Команды сборки
cd ~/Projects/WorkCalculatorFinal
source .venv/bin/activate
export PIP_BREAK_SYSTEM_PACKAGES=1
buildozer -v android debug

## Результат
APK: bin/workcalculatorapp-0.0.38-arm64-v8a_armeabi-v7a-debug.apk
Установлен на телефон ✅ РАБОТАЕТ!
