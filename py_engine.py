import pygame
from PIL import Image
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from gpiozero.exc import BadPinFactory

class Engine:
    sprites = {}

    def register_sprite(name, number):
        img = Image.open(f"assets/{name}.png").convert("RGBA").resize((5, 8))

        matrix = []
        for y in range(8):
            row = []
            for x in range(5):
                r, g, b, a = img.getpixel((x, y))
                if a > 0 and r < 128 and g < 128 and b < 128:
                    row.append(1)
                else:
                    row.append(0)
            matrix.append(row)

        Engine.sprites[number] = matrix

    def render(obj):
        result = obj.render()

        if isinstance(result, str):
            return "X"
        elif isinstance(result, int):
            if result in Engine.sprites:
                return Engine.sprites[result]
            else:
                raise ValueError(f"Sprite number {result} not registered.")

class Engine:
    class Sound:
        def __init__(self, music = 'default', soundEffects: list[str] = []):
            try: 
                self.buzzer: TonalBuzzer = TonalBuzzer(0) # TBD pin location
            except BadPinFactory:
                self.buzzer = None
                print("buzzer setup failed")
            self.currentNoteIndex = 0
            self.soundEffects = {}

            for effectName in soundEffects: 
                with open(f"assets/soundeffects/{effectName}.txt") as f:
                    notes = f.read().strip().split()
                    self.soundEffects[effectName] = { q : notes[q] for q in range(len(notes))}
                    f.close()

            with open(f"assets/music/{music}.txt") as f:
                notes = f.read().strip().split()
                self.soundtrackLength = len(notes)
                self.musicNotes = {i: notes[i] for i in range(self.soundtrackLength)}
                f.close()

        def playSoundEffect(self, effectName: str):
            if not self.buzzer:
                return
               
            effectNotes: list[str] = self.soundEffects[effectName]
            for i in range(len(effectNotes)):
                # TODO: determine transition step value to reduce choppiness
                self.buzzer.play(Tone(effectNotes[i]))   

        # play the current note of the soundtrack. cycle to beginning when finished.
        def playNote(self): 
            if not self.buzzer:
                return
            # TODO: determine transition step value to reduce choppiness
            self.buzzer.play(Tone(self.musicNotes[self.currentNoteIndex]))
            self.currentNoteIndex = (self.currentNoteIndex + 1 ) % self.soundtrackLength
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
        CELL_HEIGHT = 8
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
                draw_lcd_cell(obj.x, obj.y, Engine.render(obj))

            draw_lcd_cell(
                Engine.player.x, Engine.player.y, Engine.render(Engine.player)
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
