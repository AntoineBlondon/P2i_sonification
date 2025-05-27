Dictionnaire des 12 teintes auxquelles nous nous sommes limités chacune associée à une fréquence
(interprétation de Neil Harbinsson) 

def histogramme_couleur(Image):
    # Création du dictionnaire 
    Initialisation d’un dictionnaire vide 
    Parcours de l’image pixel par pixel (double boucle for)
        On relève la couleur du pixel : paramètre teinte en HSV 
        On trouve la fréquence associée à la couleur la plus proche dans le dictionnaire des teintes
        On incrémente la valeur associée à cette couleur 
    
    return dictionnaire


def create_notes(Image):
    # Création et enregistrement de l’accord 
    Pour chaque teinte du dictionnaire provenant de histogramme_couleur(Image)
        On relève le nombre de pixels (normalisé, entre 0 et 1)
        On définit le volume de la note correspondante par cette valeur
    On ajoute la note avec son volume à l’accord

    return accord 


def sonification_contour(Image):
    Parcours de l’image de gauche à droite par colonne (boucle for)
        Pour chaque pixel de la colonne
            Si il est blanc
                On associe sa position dans la colonne à une hauteur de note
                On ajoute la note à l’accord de la colonne	 
        On ajoute l’accord de la colonne dans une piste audio 
    return piste audio (fichier MIDI)



def convertir_en_contours(Image):
    Application d’un seuil => Passage en noir et blanc (0 et 1)
    Érosion de l’image => image sans ses contours
    Différence entre l’image et l’érosion de l’image => récupération des contours
    Redimensionnement de l’image => méthode nearest (Valeur la plus proche : pas de gris)
    return Image traitée