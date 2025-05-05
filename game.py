from board import Board

class MinesweeperGame:
    def __init__(self, width=10, height=10, num_mines=10):
        self.board = Board(width, height, num_mines)
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.game_over = False
        self.win = False
    
    def new_game(self):
        """Start a new game."""
        self.board = Board(self.width, self.height, self.num_mines)
        self.game_over = False
        self.win = False
    
    def reveal_cell(self, x, y):
        """Reveal a cell at the given coordinates."""
        if self.game_over or self.win:
            return False
        
        result = self.board.reveal_cell(x, y)
        self.game_over = self.board.game_over
        self.win = self.board.win
        
        return result
    
    def toggle_flag(self, x, y):
        """Toggle flag on a cell at the given coordinates."""
        if self.game_over or self.win:
            return False
        
        return self.board.toggle_flag(x, y)
    
    def get_board_state(self):
        """Get the current visible state of the board."""
        return self.board.get_visible_board()
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over
    
    def is_win(self):
        """Check if the game is won."""
        return self.win