# Sonification des Images

Ce projet permet de transformer des images en musique en utilisant des techniques de traitement d'image et de génération de fichiers MIDI, puis de les convertir en sons de piano. Une interface graphique simple permet de charger une image, la sonifier, et écouter le résultat.

## Fonctionnalités

* Interface graphique avec Tkinter
* Chargement d’une image en niveaux de gris
* Traitement de l’image avec Skimage pour extraire les contours
* Conversion des données visuelles en fichier MIDI
* Synthèse audio personnalisée avec un son de piano généré par synthèse additive
* Export en WAV et lecture directe

## Interface

L’interface permet :

* de charger une image (formats supportés : PNG, JPG, JPEG, BMP)
* de générer une musique à partir de l’image
* de jouer le son produit
* d’afficher les étapes du traitement d’image si l’option est activée (à compléter si le bouton de checkbox est relié)

## Structure du projet

```
sonification-des-images/
├── interface.py              # Interface utilisateur avec Tkinter
├── image_vers_son_v4.py      # Logique de traitement et conversion image → son
├── traitement.py             # Fonctions de traitement d’image pour les contours
├── color_manager.py          # Fonctions de traitement des couleurs
├── musique_manager.py        # Fonctions de synthèse de son pour les couleurs
├── images/                   # Dossier d'images de test
├── output.wav                # Exemple de sortie audio (généré après sonification)
└── README.md                 # Ce fichier
```

## Dépendances

Assurez-vous d’installer les bibliothèques suivantes :

```bash
pip install pillow numpy matplotlib pretty_midi mido scipy scikit-image
```

> Note : `aplay` (Linux) est utilisé pour jouer le son. Sur d'autres plateformes, remplacez cette ligne dans `interface.py` :

```python
os.system("aplay -q output.wav")
```

par une commande adaptée à votre système (comme `afplay` sur macOS ou `playsound` en Python multiplateforme).

## Lancement

Lancez l’interface avec :

```bash
python3 interface.py
```

Puis :

1. Cliquez sur "Charger une image" pour sélectionner un fichier.
2. Cliquez sur "Sonifier" pour générer le son.
3. Cliquez sur "Jouer" pour l’écouter.

## Comment ça marche ?

* L’image est convertie en niveaux de gris.
* Les contours sont extraits avec un filtre de Sobel.
* On applique une fermeture morphologique pour nettoyer l’image.
* L’image est réduite et seuillée, puis chaque colonne devient un accord joué à un instant donné.
* Les positions verticales sont mappées à des notes MIDI.
* Le tout est synthétisé dans un fichier MIDI, puis converti en WAV avec un synthétiseur imitant un piano.
