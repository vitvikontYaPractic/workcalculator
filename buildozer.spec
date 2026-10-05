[app]

title = Work Calculator
package.name = workcalculatorapp
package.domain = org.workcalculator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,db,ico
source.exclude_dirs = .venv,.git,.idea,bin,__pycache__,.buildozer,logs/__pycache__,database/__pycache__
source.exclude_patterns = *.backup,*.bak,*.pyc,*.log

version = 0.0.38
icon.filename = %(source.dir)s/icons/icon.png

requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor==2.0.9,asynckivy==0.6.2,loguru==0.7.2,peewee==3.17.1,pillow==10.3.0,requests,urllib3,charset-normalizer,idna,certifi,docutils,pygments,filetype,android

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b
android.ndk_path = /home/vitvikont/Android/Sdk/ndk/25.1.8937393

android.sdk_path = /home/vitvikont/Android/Sdk
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.private_storage = True
android.skip_update = True

p4a.bootstrap = sdl2
p4a.setup_py = false
p4a.branch = py311
p4a.url = file:///tmp/p4a-mirror

[buildozer]
log_level = 2
warn_on_root = 1
