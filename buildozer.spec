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

# --- LA LIGNE MAGIQUE QUI MANQUAIT ---
android.accept_sdk_license = True
# -------------------------------------

# On fixe des versions stables pour éviter les bugs des versions trop récentes
android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Important pour GitHub
p4a.branch = release-2022.12.20

[buildozer]
log_level = 2
warn_on_root = 1
