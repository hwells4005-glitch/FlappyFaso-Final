[app]
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
version = 1.0

# ON REMET KIVMOB POUR LES PUBS
requirements = python3,kivy==2.2.0,android,kivmob

# --- IMAGES DESACTIVEES POUR EVITER LE CRASH ---
# Si ça marche, on pourra les remettre plus tard
# presplash.filename = presplash.png
# icon.filename = icon.png

orientation = portrait
fullscreen = 0

# PERMISSIONS INTERNET (POUR LES PUBS)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 21

# LA PROTECTION DE LICENCE
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# DEPENDANCES ADMOB
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
