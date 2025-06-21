from PIL import Image
from RPLCD.i2c import CharLCD
import time


lcd = CharLCD(i2c_expander="PCF8574", address=0x27, port=1, cols=16, rows=2, dotsize=8)


class Engine:
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

        byte_map = [int("".join(map(str, row)), 2) for row in matrix]

        lcd.create_char(number, byte_map)

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
        return Engine.JoystickInputs(
            left=False,
            right=False,
            up=False,
            down=False,
        )

    def get_button_a():
        return False

    def get_button_b():
        return False

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

    unrendered_cells = set()

    def reset_unrendered_cells():
        Engine.unrendered_cells = set((x, y) for x in range(16) for y in range(2))

    def render_cell(cell, x, y):
        if 0 <= x < 16 and 0 <= y < 2:
            lcd.cursor_pos = (y, x)
            lcd.write_string(chr(cell) if isinstance(cell, int) else cell)
            Engine.unrendered_cells.discard((x, y))

    def run(loop):
        lcd.clear()

        while True:
            start_time = time.time()

            Engine.reset_unrendered_cells()

            loop()

            lcd.clear()

            for obj in Engine.objects:
                Engine.render_cell(obj.render(), obj.x, obj.y)

            Engine.render_cell(Engine.player.render(), Engine.player.x, Engine.player.y)

            for x, y in Engine.unrendered_cells:
                lcd.cursor_pos = (y, x)
                lcd.write_string(" ")

            Engine.unrendered_cells.clear()

            elapsed = time.time() - start_time
            if elapsed < 0.1:
                time.sleep(0.1 - elapsed)

    def reset():
        Engine.state = Engine.initial_state.copy()
        Engine.objects = []
