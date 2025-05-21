import skimage as ski
import numpy as np
from PIL import Image

"""
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

"""

def convertir_en_contour_v2(image: np.ndarray, disk_size: int=5) -> np.ndarray:
    monochrome_image = (image > ski.filters.threshold_mean(image)).astype(np.uint8)
    
    eroded_image = ski.morphology.erosion(monochrome_image, ski.morphology.disk(disk_size)).astype(np.uint8)

    outlined_image = monochrome_image - eroded_image

    resized_image = Image.fromarray(outlined_image).resize((100, 70), resample=Image.NEAREST)

    return resized_image



