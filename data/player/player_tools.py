from .. import constants as c
import pygame as pg

class Keys:
    def __init__(self, controls):
        self.controls = controls
        self.UP = controls['UP']
        self.DOWN = controls['DOWN']
        self.RIGHT = controls['RIGHT']
        self.LEFT = controls['LEFT']
        self.SWAP = controls['SWAP']
        self.GENERATE = controls['GENERATE']

    def name(self, k):
        AZERTY_CONTROLS = {'w':'z', 'q':'a', 'right shift': 'shift'}
        name = pg.key.name(k)
        name = name.replace(name, AZERTY_CONTROLS.get(name, name))
        return name

class PlayerInformation:
    def __init__(self, player):
        self.player = player
        self.style = c.DEFAULT_BTN_STYLE
        self.text = ""
        self.size = 12

    def update(self):
        pass

class CustomInformation(PlayerInformation):
    def __init__(self, player, text):
        super().__init__(player)
        self.text = text
        self.size = 10

class NameInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = 'Nom={}'.format(player.name)
        self.size = 17

class ModeInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = 'Mode={}'.format(c.MODE_NAME[player.board.speed])

class ScoreInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.size = 20

    def update(self):
        self.text = 'Score={:.0f}'.format(self.player.score)

class UpInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.size = 20

    def update(self):
        up_timer = int((self.player.board.speed-self.player.up_timer)/1000)
        self.text = 'UP={:.0f}'.format(up_timer)

class PauseInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.size = 20

    def update(self):
        pause_timer = int(self.player.pause_timer/600)
        self.text = 'PAUSE={:.0f}'.format(pause_timer)

class GameOverInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = 'GameOver'
        self.size = 20
