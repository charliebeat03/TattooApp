[app]
title = AzojuanitoP41
package.name = catalogotatuajes
package.domain = org.azojuanito

source.dir = .
source.main = main.py

version = 1.0
requirements = python3, kivy, kivymd, supabase, httpx, websockets

android.permissions = INTERNET
android.api = 30
android.minapi = 21
android.ndk_api = 21


source.include_exts = py,png,jpg,kv,atlas,ico,ttf


icon.filename = iconoTattoo.ico

[buildozer]
log_level = 2

