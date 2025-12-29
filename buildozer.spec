[app]
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3

version = 1.0
requirements = python3,kivy==2.2.0,android,ffpyplayer,ffpyplayer_codecs

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# On accepte la licence automatiquement
android.accept_sdk_license = True

# Versions Android
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# --- LA CORRECTION EST ICI ---
# On passe sur la branche principale pour avoir le support AAB
p4a.branch = master
# -----------------------------

[buildozer]
log_level = 2
warn_on_root = 1
