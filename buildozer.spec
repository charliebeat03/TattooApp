[app]
# Configuración básica de la app
title = AzojuanitoP41
package.name = azojuanitop41
package.domain = com.azojuanito

# Directorio fuente
source.dir = .

# Archivo principal
source.main = main.py

# Requisitos de la aplicación
requirements = python3, kivy, kivymd, supabase, httpx, websockets

# Configuración Android
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True

# Permisos
android.permissions = INTERNET

# Icono de la aplicación (asegúrate de tener el archivo)
icon.filename = %(source.dir)s/icon.png

# Incluir archivos KV y recursos
source.include_exts = py,png,jpg,kv,atlas,json,txt,ttf

# Log level
log_level = 2

[buildozer]
# Configuración de buildozer
log_level = 2
