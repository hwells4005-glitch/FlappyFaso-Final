[app]
title = Flappy Faso
package.name = flappyfaso
package.domain = org.faso
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
version = 1.0

# KIVMOB POUR LES PUBS
requirements = python3,kivy==2.2.0,android,kivmob

# --- CONFIG IMAGES ---
# ✅ ON GARDE L'ICONE (Il faut le fichier icon.png sur GitHub !)
icon.filename = icon.png

# ❌ ON ENLEVE LE PRESPLASH (Pour éviter les erreurs si manquant)
# presplash.filename = presplash.png

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21

# --- FIX OBLIGATOIRE (POUR CORRIGER L'ERREUR AIDL DE TES LOGS) ---
android.build_tools_version = 34.0.0
android.accept_sdk_license = True

# FIX ADMOB (CRUCIAL POUR NE PAS CRASHER)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713
android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0

android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
