from py_engine import Engine
import random

Engine.register_sprite("dino", 0)
Engine.register_sprite("cactus", 1)
Engine.register_sprite("rock", 2)
Engine.register_sprite("bird", 3)


class Player(Engine.GameObject):
    jump_time = 0

    def __init__(self):
        super().__init__(1, 1)

    def render(self):
        return 0


class Obstacle(Engine.GameObject):
    kind = "cactus"

    def __init__(self):
        self.kind = random.choice(["cactus", "rock", "bird"])
        super().__init__(15, 0 if self.kind == "bird" else 1)

    def render(self):
        match self.kind:
            case "cactus":
                return 1
            case "rock":
                return 2
            case "bird":
                return 3
            case _:
                return "X"


def loop():
    if Engine.state["otimer"] % 4 == 0:
        for obj in Engine.get_objects_of(Obstacle):
            obj.x -= 1

    if Engine.state["otimer"] == 0:
        Engine.new_object(Obstacle())
        Engine.state["otimer"] = 20

    Engine.state["otimer"] -= 1

    if Engine.player.jump_time > 0:
        Engine.player.jump_time -= 1
    elif Engine.get_button_a():
        Engine.player.jump_time = 8

    Engine.player.y = 0 if Engine.player.jump_time > 0 else 1

    for obj in Engine.get_objects_of(Obstacle):
        if Engine.player.x == obj.x and Engine.player.y == obj.y:
            Engine.reset()
            Engine.player.jump_time = 0


# Start the game

Engine.set_state(
    {
        "otimer": 0,  # Obstacle timer
    }
)
Engine.set_player(Player())
Engine.run(loop)
