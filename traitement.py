import skimage as ski
import numpy as np
from PIL import Image

def contour(image: np.ndarray) -> np.ndarray:
    return ski.filters.sobel(image)


def apply_threshold(image: np.ndarray) -> np.ndarray:
    return image > ski.filters.threshold_mean(image)

def fermeture(image: np.ndarray, disk_size: int=2) -> np.ndarray:
    return ski.morphology.closing(image, footprint=ski.morphology.disk(disk_size))


def ouverture(image: np.ndarray, disk_size: int=2) -> np.ndarray:
    return ski.morphology.opening(image, footprint=ski.morphology.disk(disk_size))


def convertir_en_contour(image: np.ndarray) -> np.ndarray:
    temp_image = contour(apply_threshold(image))
    temp_image = fermeture(temp_image, 5)
    temp_image = Image.fromarray(temp_image).resize((100, 70))
    temp_image = apply_threshold(np.asarray(temp_image))
    return temp_image