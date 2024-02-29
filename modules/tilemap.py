import pygame
NEIGHBOR_OFFSET = [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(0,0),(-1,1),(0,1),(1,1),]
COLLIDABLE_TILE_TYPES = {"grass", "stone"}
from modules.utils import sum_vectors, k_vector
import json


def pos_in_pixels(posicao_tilemap, tile_size=16):
    """retorna a posicao em pixels a partir da posicao no tilemap"""
    return tuple(map(lambda x: x*tile_size, posicao_tilemap))

class Tilemap:
    def __init__(self, game, map_filename="", tile_size=16):
        self.game = game
        self.tile_size = tile_size
        #temos dois sistemas: um que é em uma grid (grade)
        self.tilemap = {}
        #e outro que pode nao estar alinhado à grade
        #esses offgrids sao decoracoes, background, basicamente
        self.offgrid_tiles = []


        # preenchendo o mapa
        if map_filename:
            #abrindo o arquivo e carregando as informacoes
            with open(map_filename, "r") as map_F:
                raiz = json.loads(map_F.read())
                tilemap_arquivo = raiz['tilemap']
                #mudar esta linha pra ler o tile_size do arquivo
                tile_size = raiz['tile_size']
                offgrid_tilemap = raiz['offgrid']

            #guardando os tiles do arquivo no nosso tilemap
            #observe que cada tile esta armazenado num dicionario cuja chave é a coordenada e os valore sao {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}  
            for coordenada in tilemap_arquivo:
                self.tilemap[coordenada] = tilemap_arquivo[coordenada]      
        else:
            #preenchendo da maneira padrao
            for i in range(10):
                self.tilemap[str(3 + i) + ";10"] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
                self.tilemap["10;" + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}       

    def __dump_map__(self):
        newmap_filename = "newmap.json"
        raiz = {}
        raiz['tile_size'] = self.tile_size
        raiz['tilemap'] = self.tilemap
        raiz['offgrid'] = []
        with open(newmap_filename, "w") as file:
            json.dump(raiz, file)

    def neighbor_tiles(self, pos):
        """Retorna uma lista com no máximo todos os 9 blocos ao redor do personagem, se existirem"""
        # a posicao esta em pixel, passemos-na pra posicao em tiles
        tile_position = tuple(map (lambda axis:(int(axis // self.tile_size)), pos))
        tiles = []
        for offset in NEIGHBOR_OFFSET:
            possible_block = str(tile_position[0] + offset[0]) + ";" + str(tile_position[1] + offset[1])
            if possible_block in self.tilemap:
                tiles.append(self.tilemap[possible_block])
        return tiles

    def physics_rects_around(self, pos):
        """Retorna a lista dos retangulos colidiveis ao nosso redor"""
        rects = []
        for tile in self.neighbor_tiles(pos):
            if tile['type'] in COLLIDABLE_TILE_TYPES:
                rects.append(pygame.Rect(*pos_in_pixels(tile['pos']), self.tile_size, self.tile_size ))
        return rects
    
    def render(self, surface: pygame.Surface, offset=(0,0)):
        
        for tile in self.offgrid_tiles:
            #interpretaremos a posicao como PIXEL, nao como lugar na grid
            surface.blit(self.game.assets[tile['type']][tile['variant']],sum_vectors( k_vector(-1, offset), tile['pos']) )

        start_screen_x, end_screen_x = offset[0]//self.tile_size, (offset[0] + surface.get_width()) // self.tile_size
        #start_screen_y, end_screen_y = offset[1]//self.tile_size, (offset[1] + surface.get_height()) // self.tile_size


        for loc in self.tilemap:
            
            #pega a lista de assets daquele tipo, acessa o indice (variant) dela e desenha
            #apenas os tiles que estao dentro da tela (entre o inicio e o final dela)
            #nao é a melhor otimizacoa, no youtube deve ter coisa melhor
            tile = self.tilemap[loc]
            tile_x, tile_y = tile['pos'] 
            if tile_x >= start_screen_x  and tile_x <= end_screen_x:
                #pegar a imagem dos assets daquele tipo (grass):  tile['type]
                #pegar a imagem de numero = variant (1) desta lista
                # e desenhá-la na tela
                surface.blit(self.game.assets[tile['type']][tile['variant']],
                            sum_vectors(k_vector(-1, offset), 
                            pos_in_pixels(tile['pos'])
                            ))


