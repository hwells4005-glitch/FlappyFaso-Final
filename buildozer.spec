[app]

# Titre de l'application
title = Flappy Faso

# Nom du package
package.name = flappyfaso

# Domaine du package
package.domain = com.fasolab

# Version du code source
version = 1.0.0

# Numéro de version
version.code = 1

# Auteur
author = Faso Lab

# Chemin du code source
source.dir = .

# Point d'entrée principal
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,json

# Application principale
main = main.py

# Version de Python
python.version = 3.9

# Version de Android SDK
android.sdk = 28
android.ndk = 23b
android.ndk_api = 21

# Permissions Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# Caractéristiques
android.features = android.hardware.screen.portrait

# API minimum
android.minapi = 21

# API cible
android.targetapi = 33

# Orientation
orientation = portrait

# Plein écran
fullscreen = 1

# Prévention du sommeil
wake_lock = 1

# Accélération matérielle
android.accelerometer = 1

# Rendu
graphics = opengl

# Rétention de données
android.preserve_paths = assets/%,data/%

# Bibliothèques requises
requirements = python3,kivy==2.3.0,kivymd,kivmob,Pillow

# Bibliothèques Android
android.gradle_dependencies = com.google.android.gms:play-services-ads:22.0.0

# Services Google
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-3940256099942544~3347511713

# Buildozer
p4a.branch = develop

# Log level
log_level = 2

# Icones
icon.fg.png = assets/icon.png
icon.fg.color = white

# Lancement d'images
presplash.fg.png = assets/presplash.png
presplash.fg.color = white

# Build
build = debug

# Architecture
android.arch = arm64-v8a,armeabi-v7a

[buildozer]

# Configuration de log
log_level = 2
warn_on_root = 1
