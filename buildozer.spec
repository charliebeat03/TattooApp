[app]
# (str) Title of your application
title = AzojuanitoP41

# (str) Package name
package.name = azojuanitop41

# (str) Package domain (needed for android/ios packaging)
package.domain = com.azojuanito

# (str) Source code where the main.py live
source.dir = .

# (list) Application requirements
requirements = python3, kivy, kivymd, supabase, httpx, websockets

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license agreements.
android.accept_sdk_license = True

# (list) Permissions
android.permissions = INTERNET
