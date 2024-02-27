class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        #temos dois sistemas: um que é em uma grid (grade)
        self.tilemap = {}
        #e outro que pode nao estar alinhado à grade
        #esses offgrids sao decoracoes, background, basicamente
        self.offgrid_tiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap["10;" + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}            
        
    def render(self, surface):
        
        for tile in self.offgrid_tiles:
            #interpretaremos a posicao como PIXEL, nao como lugar na grid
            surface.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            #pega a lista de assets daquele tipo, acessa o indice (variant) dela e desenha
            surface.blit(self.game.assets[tile['type']][tile['variant']], 
                         tuple(map(lambda x: x*self.tile_size, tile['pos'])))
        
