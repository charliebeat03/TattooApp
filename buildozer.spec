[app]

# Título y paquete de la aplicación
title = AzojuanitoP41
package.name = catalogotatuajes
package.domain = org.azojuanito

# Ruta del código fuente
source.dir = .
source.main = main.py

# Versión
version = 1.0

# Requisitos (las librerías que usa tu app)
requirements = python3, kivy, kivymd, supabase, httpx, websockets

# Configuración de Android
android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b

# Archivos a incluir (asegúrate de que tu icono esté en la misma carpeta)
source.include_exts = py,png,jpg,kv,atlas,ico,ttf
icon.filename = iconoTattoo.ico

# Orientación de la pantalla
orientation = portrait
