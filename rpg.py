from engine import Engine


class Player(Engine.GameObject):
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


class Enemy(Engine.GameObject):
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


def loop():
    old_player_pos = [Engine.player.x, Engine.player.y]

    def reset_player_pos():
        Engine.player.x = old_player_pos[0]
        Engine.player.y = old_player_pos[1]

    js = Engine.get_joystick()

    if js.left:
        Engine.player.x = max(0, Engine.player.x - 1)
    if js.right:
        Engine.player.x = min(15, Engine.player.x + 1)
    if js.up:
        Engine.player.y = max(0, Engine.player.y - 1)
    if js.down:
        Engine.player.y = min(1, Engine.player.y + 1)

    for enemy in Engine.get_objects_of(Enemy):
        if enemy.x == Engine.player.x and enemy.y == Engine.player.y:
            enemy.health -= 1
            reset_player_pos()

            if enemy.health == 0:
                Engine.delete_object(enemy)


Engine.new_object(Kobold(x=7, y=0))
Engine.new_object(Kobold(x=12, y=1))
Engine.set_player(Player())
Engine.run(loop)
