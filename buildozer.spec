[app]

# (str) Title of your application
title = Flappy Faso

# (str) Package name
package.name = flappyfaso

# (str) Package domain (needed for android/ios packaging)
package.domain = org.faso

# (str) Source code where the main.py live
source.dir = .

# (str) Source files to include (let empty to include all the files)
# On inclut bien les WAV pour les sons
source.include_exts = py,png,jpg,kv,atlas,wav

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# KivMob est nécessaire pour les pubs
requirements = python3,kivy==2.2.0,android,kivmob

# (str) Presplash of the application
# On garde les défauts pour éviter les erreurs d'images manquantes pour l'instant
# presplash.filename = presplash.png
# icon.filename = icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# OBLIGATOIRE POUR ADMOB
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# --- FIX 1 : LA PROTECTION DE LICENCE ---
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# --- FIX 2 : LA LIGNE MANQUANTE (CAUSE DU CRASH) ---
# Sans cette ligne, AdMob fait crasher l'appli au démarrage !
# C'est l'ID de TEST de Google.
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (list) List of Gradle dependencies to add
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) python-for-android branch to use, defaults to master
p4a.branch = master


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
