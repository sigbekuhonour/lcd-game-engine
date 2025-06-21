import pygame


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
    return JoystickInputs(
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
