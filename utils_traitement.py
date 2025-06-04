import skimage as ski
import numpy as np
from PIL import Image


def convertir_en_contour(image: np.ndarray, disk_size: int=5) -> np.ndarray:
    """Traite l'image pour récupérer les contours

    Etapes :
    1. Transforme l'image en noir et blanc avec un seuillage
    2. Erode l'image
    3. On calcule la différence entre l'image et son érosion pour garder uniquement les contours
    4. On change la taille de l'image

    Args:
        image (np.ndarray): L'image à traiter
        disk_size (int, optional): La taille du disque pour l'érosion. Defaults to 5.

    Returns:
        np.ndarray: L'image traitée
    """
    monochrome_image = (image > ski.filters.threshold_mean(image)).astype(np.uint8)
    
    eroded_image = ski.morphology.erosion(monochrome_image, ski.morphology.disk(disk_size)).astype(np.uint8)

    outlined_image = monochrome_image - eroded_image

    resized_image = Image.fromarray(outlined_image).resize((100, 70), resample=Image.NEAREST)

    return resized_image



