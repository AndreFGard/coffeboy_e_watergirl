class Game(modules.input.Input):
    def __init__(self):
        modules.input.Input.__init__(self)
        self.width = 1280
        self.height = 960
        self.is_fullscreen = False
    
        pygame.init()
        pygame.display.set_caption("coffeboy e watergirl")

        self.screen = pygame.display.set_mode((self.width, self.height))
        #gera uma imagem. Pra aumentar o tamanho das coisas na tela,
        #renderizamos nela e depois escalamos pra screen 
        #é no display que gravaremos as coisas
        self.display = pygame.Surface((320, 240))