
import pygame
import os

BASE_IMG_PATH =  "data/images/"


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

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images

def distance(A, B): 
    return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5


class Animation:
    def __init__(self, images: list[pygame.Surface], img_dur=5, loop=True):
        self.images = images
        # a animacao durara por 5 * len(self.images)
        self.img_dur=5

        #se queremos loopar a naimacao
        self.loop = loop
        self.done = False
        self.frame = 0
        
        #tamanho, pra quando ele nao for fornecido
        self.size = images[0].get_size()
    
    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def get_size(self):
        return self.images[0].get_size()
    
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

def load_assets():
    return {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'tea' : load_images('tiles/tea'),
            'player': load_image("entities/player/idle/00.png"),
            'background': load_image("Background2.png"),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=4),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=4),
            'moeda/idle': Animation(load_images("coins"), img_dur=4),
            'moeda': load_image("coins/00.png"),
            'grao_de_cafe': load_image("hud/inventory/coffee_beans/00.png"),
            'grao_de_cafe/idle':Animation([pygame.transform.scale(load_image("hud/inventory/coffee_beans/00.png"), (17,17))]),
            'agua_quente': load_image("hud/inventory/water_cup/00.png"),
            'agua_quente/idle':Animation([pygame.transform.scale(load_image("hud/inventory/water_cup/00.png"), (17,17))]),
            'botas': load_image("buffs/boots/00.png"),
            'botas/idle':Animation([pygame.transform.scale(load_image("buffs/boots/00.png"), (17,17))]),
            'raio': load_image("buffs/lightning/00.png"),
            'raio/idle':Animation([pygame.transform.scale(load_image("buffs/lightning/00.png"), (17,17))]),
            'walls': load_images("tiles/walls"),
            'tea/idle':Animation(load_images('entities/tea/idle')),

            'copo_de_cafe': load_image("buffs/coffee/00.png"),
            'copo_de_cafe/idle':Animation([pygame.transform.scale(load_image("buffs/coffee/00.png"), (17,17))]),
            }

def get_pos_from_tilemap_pos(pos):
    return k_vector(16, pos)