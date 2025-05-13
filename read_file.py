import pygame

pygame.init()

pygame.mixer.music.load("image_musique.mid")

pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)