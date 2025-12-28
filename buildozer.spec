[app]
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
version = 1.0
# INCLUT FFPYPLAYER POUR LE SON
requirements = python3,kivy==2.2.0,android,ffpyplayer,ffpyplayer_codecs
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = release-2022.12.20
[buildozer]
log_level = 2
warn_on_root = 1
