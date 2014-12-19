from .. import constants as c

class Keys:
    def __init__(self, controls):
        self.UP = controls['UP']
        self.DOWN = controls['DOWN']
        self.RIGHT = controls['RIGHT']
        self.LEFT = controls['LEFT']
        self.SWAP = controls['SWAP']
        self.GENERATE = controls['GENERATE']

class PlayerInformation:
    def __init__(self, player):
        self.player = player
        self.style = c.DEFAULT_BTN_STYLE
        self.text = ""

    def update(self):
        pass

class CustomInformation(PlayerInformation):
    def __init__(self, player, text):
        super().__init__(player)
        self.text = text

class NameInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = '{}: {}'.format(player.index, player.name)

class ModeInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = '{}'.format(c.MODE_NAME[player.board.speed])

class ScoreInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        self.text = 'Score={:.0f}'.format(self.player.score)

class UpInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        #pause_timer = int(self.player.pause_timer/600)
        up_timer = int(self.player.up_timer/1000)
        self.text = 'UP={:.0f}'.format(up_timer)

class PauseInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)

    def update(self):
        pause_timer = int(self.player.pause_timer/600)
        self.text = 'PAUSE={:.0f}'.format(pause_timer)

class GameOverInformation(PlayerInformation):
    def __init__(self, player):
        super().__init__(player)
        self.text = 'GameOver'
