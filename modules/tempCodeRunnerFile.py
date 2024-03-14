font = pygame.font.Font(None, 36)
                quantity_text = font.render(str(slot.quantity), True, (0, 0, 0))
                quantity_rect = quantity_text.get_rect(center=(item_x + 15, item_y + 15))