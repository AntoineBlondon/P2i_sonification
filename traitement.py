from skimage.io import imread
import skimage as ski
import scipy as sci
import skimage as ski
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def contour(image: np.ndarray) -> np.ndarray:
    return ski.filters.sobel(image)


def apply_threshold(image: np.ndarray) -> np.ndarray:
    return image > ski.filters.threshold_mean(image)

def fermeture(image: np.ndarray) -> np.ndarray:
    return ski.morphology.opening(image, footprint=ski.morphology.disk(2))


if __name__ == "__main__":


    I = imread('bird.jpg', as_gray=True)
    print(len(I))

    I = fermeture(apply_threshold(contour(I)))

    plt.imshow(I, cmap="gray")
    plt.show()