import skimage as ski
import numpy as np


def contour(image: np.ndarray) -> np.ndarray:
    return ski.filters.sobel(image)


def apply_threshold(image: np.ndarray) -> np.ndarray:
    return image > ski.filters.threshold_mean(image)

def fermeture(image: np.ndarray, disk_size: int=2) -> np.ndarray:
    return ski.morphology.closing(image, footprint=ski.morphology.disk(disk_size))


def ouverture(image: np.ndarray, disk_size: int=2) -> np.ndarray:
    return ski.morphology.opening(image, footprint=ski.morphology.disk(disk_size))
