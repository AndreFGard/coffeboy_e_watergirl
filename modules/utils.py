BASE_IMG_PATH =  "data/images/"
import pygame

def sum_vectors(v1:tuple, v2:tuple) -> tuple:
    """Sums the corresponding indexes of the vectors"""
    if len(v1) == 2:
        return v1[0] + v2[0], v1[1] + v2[1]
    
def subtract_vectors(v, w):
    "returns v - w"
    return v[0] - w[0], v[1] - w[1]

def k_vector(k, v):
    """multiplica o vetor por um escalar"""
    return (k*v[0], k*v[1])

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

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        # a animacao durara por 5 * len(self.images)
        self.img_dur=5

        #se queremos loopar a naimacao
        self.loop = loop
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            #isto GARANTE que nao iremos pegar um frame a mais do que devemos, mas sim que
            # iremos reiniciar
            self.frame =(self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) -1)
            if self.frame >= self.img_dur * len(self.images) -1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_dur)]