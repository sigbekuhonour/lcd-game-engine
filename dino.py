import engine
import random


class Player(engine.GameObject):
    jump_time = 0

    def __init__(self):
        super().__init__(1, 1)

    def render(self):
        return [
            [0, 0, 1, 1, 1],
            [0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 1, 0, 0],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 0, 0],
            [1, 0, 1, 0, 0],
        ]


class Obstacle(engine.GameObject):
    kind = "CACTUS"

    def __init__(self):
        self.kind = random.choice(["CACTUS", "ROCK", "BIRD"])
        super().__init__(15, 0 if self.kind == "BIRD" else 1)

    def render(self):
        if self.kind == "CACTUS":
            return [
                [0, 0, 1, 0, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1],
                [1, 1, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
            ]

        if self.kind == "ROCK":
            return [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 1, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ]

        if self.kind == "BIRD":
            return [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 1, 0, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0],
            ]


player = Player()
objects = [player]
obstacle_timer = 0


def tick():
    global obstacle_timer
    global objects

    if obstacle_timer % 4 == 0:
        for obj in objects:
            if isinstance(obj, Obstacle):
                obj.x -= 1

    if obstacle_timer == 0:
        objects.append(Obstacle())
        obstacle_timer = 20

    obstacle_timer -= 1

    if player.jump_time > 0:
        player.jump_time -= 1
    elif engine.get_button_a():
        player.jump_time = 8

    player.y = 0 if player.jump_time > 0 else 1

    for obj in objects:
        if isinstance(obj, Obstacle):
            if player.x == obj.x and player.y == obj.y:
                objects = [player]
                obstacle_timer = 0

    return objects
