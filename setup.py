#!/usr/bin/env python3
"""
Script d'installation pour Flappy Faso
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Vérifie et installe les dépendances"""
    required = [
        'kivy==2.3.0',
        'kivymd',
        'kivmob',
        'Pillow',
    ]
    
    print("Installation des dépendances...")
    for package in required:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_directories():
    """Crée la structure de répertoires"""
    directories = [
        'assets/sounds',
        'assets/fonts',
        'data',
        'utils'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Créé: {directory}")

def download_resources():
    """Télécharge les ressources manquantes"""
    print("\nTéléchargez les ressources manquantes:")
    print("1. Sons: https://freesound.org/")
    print("2. Police Poppins: https://fonts.google.com/specimen/Poppins")
    print("3. Icône: Créez une icône 512x512")
    print("\nPlacez-les dans les dossiers assets/ correspondants")

def main():
    """Fonction principale"""
    print("=== Installation de Flappy Faso ===")
    
    try:
        create_directories()
        check_dependencies()
        download_resources()
        
        print("\n=== Installation terminée ===")
        print("Pour exécuter: python main.py")
        print("Pour compiler: buildozer android debug")
        
    except Exception as e:
        print(f"Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
