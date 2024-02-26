def distance(A, B): return (sum(((B[i] - A[i])**2 for i in range(2))))**0.5

class Game:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.velocity = 5 
        self.jumpcount = 10
        self.isJumping = False
        self.negative = 1 
        
    def run(self):
        import pygame

        pygame.init()

        screen = pygame.display.set_mode((self.width, self.height))
        #display = pygame.Surface((700, 700)) ???
        screen.fill((200,200,255))
        keep_running = True
        las_pressed_pos = tuple()
        player_x, player_y = self.width // 2, self.height // 2

        while keep_running:
            screen.fill((200,200,255))

            pygame.time.delay(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_running = False

                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if not las_pressed_pos: las_pressed_pos = mouse_pos
                    if distance(las_pressed_pos, mouse_pos) > 100:
                        pygame.draw.circle(screen, (240, 0, 0),mouse_pos, 20, 5)
                        las_pressed_pos = mouse_pos
            

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x -= self.velocity
            if keys[pygame.K_DOWN]:
                player_y += self.velocity            
        
            if keys[pygame.K_SPACE]:
                self.isJumping = True

            if self.isJumping:
                if self.jumpcount >= -10:
                    if self.jumpcount < 0:
                        self.negative = -1
                    player_y -= (self.jumpcount ** 2 ) * self.negative
                    self.jumpcount -= 1 
                else:
                    self.isJumping = False
                    self.jumpcount = 10
                    self.negative = 1


            pygame.draw.rect(screen, (255,0,0), (player_x, player_y, 10, 16))

            pygame.display.update()












Game().run()