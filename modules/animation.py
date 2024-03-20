
import pygame


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

