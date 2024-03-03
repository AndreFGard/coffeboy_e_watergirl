image_position = (100, 100)
            image = pygame.image.load("./data/images/hud/inventory/coffee-beans.png")
            # Desenhe a imagem na tela na posição específica
            self.display.blit(image, image_position)

            # Atualize a tela
            pygame.display.flip()