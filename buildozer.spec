[app]
title = AzojuanitoP41
package.name = catalogotatuajes
package.domain = org.azojuanito

source.dir = .
source.main = main.py

version = 1.0
requirements = python3, kivy, kivymd, supabase, httpx, websockets

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 31

# Aceptar licencias automáticamente :cite[2]
android.accept_sdk_license = True

source.include_exts = py,png,jpg,kv,atlas,ico,ttf

[buildozer]
log_level = 2
