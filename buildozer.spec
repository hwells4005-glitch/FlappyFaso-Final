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
source.include_exts = py,png,jpg,kv,atlas,wav

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.0,android,kivmob

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
presplash.filename = presplash.png

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# --- CORRECTION DE L'ERREUR DE BUILD ICI ---
# On force une version stable des outils pour éviter le bug de licence
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# (list) List of Gradle dependencies to add
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (Android API >= 23)
android.allow_backup = True

# (str) python-for-android branch to use, defaults to master
p4a.branch = master

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
