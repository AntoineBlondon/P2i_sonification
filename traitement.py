import skimage as ski
import numpy as np
from PIL import Image


def convertir_en_contour_v2(image: np.ndarray, disk_size: int=5) -> np.ndarray:
    monochrome_image = (image > ski.filters.threshold_mean(image)).astype(np.uint8)
    
    eroded_image = ski.morphology.erosion(monochrome_image, ski.morphology.disk(disk_size)).astype(np.uint8)

    outlined_image = monochrome_image - eroded_image

    resized_image = Image.fromarray(outlined_image).resize((100, 70), resample=Image.NEAREST)

    return resized_image



