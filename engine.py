import pygame
from PIL import Image


def handle_render(rendered):
    if isinstance(rendered, list):
        return rendered
    elif isinstance(rendered, str):
        img = Image.open(f"assets/{rendered}.png").convert("RGBA").resize((5, 7))
        matrix = []
        for y in range(7):
            row = []
            for x in range(5):
                r, g, b, a = img.getpixel((x, y))
                if a > 0 and r < 128 and g < 128 and b < 128:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)

        return matrix
    else:
        raise ValueError("Unsupported render type")


class Engine:
    class GameObject:
        x = 0
        y = 0

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def render(self):
            return [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ]

    class JoystickInputs:
        left = False
        right = False
        up = False
        down = False

        def __init__(self, left, right, up, down):
            self.left = left
            self.right = right
            self.up = up
            self.down = down

    def get_joystick():
        keys = pygame.key.get_pressed()
        return Engine.JoystickInputs(
            left=keys[pygame.K_a],
            right=keys[pygame.K_d],
            up=keys[pygame.K_w],
            down=keys[pygame.K_s],
        )

    def get_button_a():
        keys = pygame.key.get_pressed()
        return keys[pygame.K_j]

    def get_button_b():
        keys = pygame.key.get_pressed()
        return keys[pygame.K_l]

    objects = []

    def set_state(state):
        Engine.initial_state = state.copy()
        Engine.state = state

    def set_player(obj):
        Engine.player = obj

    def new_object(obj):
        Engine.objects.append(obj)

    def delete_object(obj):
        Engine.objects = [o for o in Engine.objects if o != obj]

    def get_objects_of(class_name):
        return [obj for obj in Engine.objects if isinstance(obj, class_name)]

    def run(loop):
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

            loop()

            for obj in Engine.objects:
                draw_lcd_cell(obj.x, obj.y, handle_render(obj.render()))

            draw_lcd_cell(
                Engine.player.x, Engine.player.y, handle_render(Engine.player.render())
            )

            # Scale up the lcd_surface and blit to the screen
            scaled_surface = pygame.transform.scale(
                lcd_surface, (WINDOW_WIDTH * SCALE, WINDOW_HEIGHT * SCALE)
            )
            screen.blit(scaled_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(100)

    def reset():
        Engine.state = Engine.initial_state.copy()
        Engine.objects = []
