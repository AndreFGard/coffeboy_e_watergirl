BASE_IMG_PATH =  "data/images/"
import pygame

def sum_vectors(v1:tuple, v2:tuple) -> tuple:
    """Sums the corresponding indexes of the vectors"""
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]

def load_image(path):
    """Carrega a imagem e seta o seu background como transparente usando o set_colorkey"""
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    #isso seta tudo o que for preto na foto como transparente
    img.set_colorkey((0,0,0))
    return img

import os
def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images