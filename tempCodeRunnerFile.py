def main_menu(self):
        color = (255,255,255)  
        color_light = (170,170,170)  
        color_dark = (100,100,100)  
        width = 1280
        height = 960
        smallfont = pygame.font.SysFont('Corbel',50)  

        buttons = [
            {"text": "Start", "position": (width/2, height/2 - 75)},
            {"text": "Quit", "position": (width/2, height/2 + 25)}
        ]

        while True:
            self.screen.fill((60,25,60))
            mouse = pygame.mouse.get_pos()

            for button in buttons:
                text_rendered = smallfont.render(button["text"], True, color)
                text_rect = text_rendered.get_rect(center=button["position"])

                if text_rect.collidepoint(mouse):
                    pygame.draw.rect(self.screen, color_light, text_rect)
                else:
                    pygame.draw.rect(self.screen, color_dark, text_rect)

                self.screen.blit(text_rendered, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        text_rect = smallfont.render(button["text"], True, color).get_rect(center=button["position"])
                        if text_rect.collidepoint(event.pos):
                            if button["text"] == "Quit":
                                pygame.quit()
                                sys.exit()
                            elif button["text"] == "Start":
                                print("Starting the game...")
                                Game.run(self)

            pygame.display.update()