class Player:

    INDEX = 0

    def __init__(self, index):
        self.index = index
        self.controls = c.CONTROLS[index]
        self.hidden_timer = 0

    def setup_game(self, board, board_gfx, keys):
        self.board = board
        self.cursor = self.board.cursor
        self.keys = keys
        self.board_gfx = board_gfx
        self.pause = 0
        self.blocks_gfx = pg.sprite.LayeredDirty()
        self.cursor_gfx = pg.sprite.LayeredDirty()
        self.info_gfx = pg.sprite.LayeredDirty()
        self.info = {}
        cursor = CursorGFX(self.cursor, board_gfx)
        cursor.add(self.cursor_gfx)
        self.alive = True
        self.score = 0
        self.setup_blocks()
        self.keys_move = [keys['UP'], keys[
            'DOWN'], keys['LEFT'], keys['RIGHT']]

    def setup_blocks(self):
        board = self.board
        for row in reversed(range(board.num_row)):
            for col in range(board.num_col):
                if board.board[row][col].color:
                    block = BlockGFX(board.board[row][col], self)
                    block.add(self.blocks_gfx)
