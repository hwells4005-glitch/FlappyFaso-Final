[app]
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
# ON RETIRE LES LIBS AUDIO LOURDES POUR CE TEST
requirements = python3,kivy==2.2.0,android

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# On accepte la licence
android.accept_sdk_license = True

# Versions Android
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Branche principale
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
