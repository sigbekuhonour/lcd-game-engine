import engine


class Player(engine.GameObject):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)

    def render(self):
        return [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ]


class Enemy(engine.GameObject):
    def __init__(self, x=0, y=0, health=1):
        super().__init__(x, y)
        self.health = health


class Kobold(Enemy):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, 2)

    def render(self):
        return [
            [1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]


player = Player()
objects = [player, Kobold(x=7, y=0), Kobold(x=12, y=1)]


def tick():
    global objects

    js = engine.get_joystick()

    old_player_pos = [player.x, player.y]

    def reset_pos():
        player.x = old_player_pos[0]
        player.y = old_player_pos[1]

    if js.left:
        player.x = max(0, player.x - 1)
    if js.right:
        player.x = min(15, player.x + 1)
    if js.up:
        player.y = max(0, player.y - 1)
    if js.down:
        player.y = min(1, player.y + 1)

    for obj in objects:
        if isinstance(obj, Enemy) and obj.x == player.x and obj.y == player.y:
            obj.health -= 1
            reset_pos()

            if obj.health == 0:
                # Delete enemy
                objects = [o for o in objects if o != obj]

    return objects
