[app]
# 1. IDENTITÉ
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav

version = 2.5

# 2. LES IMAGES (C'est ici que la magie opère !)
icon.filename = icon.png
presplash.filename = presplash.png

# 3. MOTEUR LÉGER (Sans bug)
requirements = python3,kivy==2.2.0,android

# 4. CONFIGURATION ÉCRAN
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
