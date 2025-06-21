import importlib
import pygame


def main(tick):
    CELL_WIDTH = 5
    CELL_HEIGHT = 7
    BORDER = 1
    COLS = 16
    ROWS = 2

    BG = (8, 90, 110)

    SCALE = 8  # Scale factor

    WINDOW_WIDTH = COLS * (CELL_WIDTH + BORDER) + BORDER
    WINDOW_HEIGHT = ROWS * (CELL_HEIGHT + BORDER) + BORDER

    pygame.init()
    # Create a small surface for drawing, then scale it up to the window
    lcd_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen = pygame.display.set_mode((WINDOW_WIDTH * SCALE, WINDOW_HEIGHT * SCALE))
    pygame.display.set_caption("16x2 LCD Display")

    def draw_lcd_cell(col, row, bits, bg=BG):
        x = BORDER + col * (CELL_WIDTH + BORDER)
        y = BORDER + row * (CELL_HEIGHT + BORDER)
        pygame.draw.rect(lcd_surface, bg, (x, y, CELL_WIDTH, CELL_HEIGHT))

        for row_idx in range(CELL_HEIGHT):
            for col_idx in range(CELL_WIDTH):
                if bits[row_idx][col_idx] == 1:
                    rect = pygame.Rect(x + col_idx, y + row_idx, 1, 1)
                    pygame.draw.rect(lcd_surface, (255, 255, 255), rect)

    def clear_lcd(bg=BG):
        lcd_surface.fill((4, 72, 89))

        for row in range(ROWS):
            for col in range(COLS):
                draw_lcd_cell(
                    col,
                    row,
                    [[0 for _ in range(CELL_WIDTH)] for _ in range(CELL_HEIGHT)],
                    bg=bg,
                )

    clear_lcd()
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clear_lcd()

        objects = tick()
        for obj in objects:
            draw_lcd_cell(obj.x, obj.y, obj.render())

        # Scale up the lcd_surface and blit to the screen
        scaled_surface = pygame.transform.scale(
            lcd_surface, (WINDOW_WIDTH * SCALE, WINDOW_HEIGHT * SCALE)
        )
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(100)


if __name__ == "__main__":
    game = input("What game would you like to play? ")
    tick = importlib.import_module(game).tick

    main(tick)
