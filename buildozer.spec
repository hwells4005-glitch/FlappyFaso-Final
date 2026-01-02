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
# IMPORTANT : On inclut py, images, kv, atlas et les sons wav
source.include_exts = py,png,jpg,kv,atlas,wav

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# KivMob est nécessaire pour les pubs
requirements = python3,kivy==2.2.0,android,kivmob

# (str) Presplash of the application
# L'image de chargement (Assure-toi d'avoir le fichier presplash.png sur GitHub !)
presplash.filename = presplash.png

# (str) Icon of the application
# L'icône de l'appli (Assure-toi d'avoir le fichier icon.png sur GitHub !)
icon.filename = icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# OBLIGATOIRE POUR QUE LES PUBS FONCTIONNENT
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# --- FIX 1 : LA PROTECTION DE LICENCE ---
# Force une version stable pour éviter l'erreur "Aidl not found"
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# --- FIX 2 : LA LIGNE ANTI-CRASH (METADATA) ---
# C'est l'ID de TEST de Google. Indispensable pour ne pas planter au démarrage.
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# (list) List of Gradle dependencies to add
# Le moteur de pub Google
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
