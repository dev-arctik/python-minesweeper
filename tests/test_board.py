import unittest
from board import Board

class TestBoard(unittest.TestCase):
    def test_board_initialization(self):
        """Test that the board initializes correctly."""
        board = Board(10, 10, 15)
        self.assertEqual(board.width, 10)
        self.assertEqual(board.height, 10)
        self.assertEqual(board.num_mines, 15)
        self.assertFalse(board.first_move_made)
        self.assertFalse(board.game_over)
        self.assertFalse(board.win)
    
    def test_place_mines(self):
        """Test that mines are placed correctly."""
        board = Board(10, 10, 15)
        board.place_mines(5, 5)  # Place mines, first click at (5, 5)
        
        # Count mines
        mine_count = 0
        for y in range(board.height):
            for x in range(board.width):
                if board.grid[y][x].is_mine:
                    mine_count += 1
        
        self.assertEqual(mine_count, 15)
        
        # Check that first click and adjacent cells are safe
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = 5 + dx, 5 + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    self.assertFalse(board.grid[ny][nx].is_mine)
    
    def test_reveal_cell(self):
        """Test revealing cells."""
        board = Board(10, 10, 15)
        # First reveal always succeeds and places mines
        self.assertTrue(board.reveal_cell(5, 5))
        self.assertTrue(board.first_move_made)
        
        # Can't reveal flagged cells
        x, y = 0, 0
        while board.grid[y][x].is_mine:  # Find a non-mine cell
            x = (x + 1) % 10
        
        board.grid[y][x].is_flagged = True
        self.assertFalse(board.reveal_cell(x, y))
        self.assertFalse(board.grid[y][x].is_revealed)
    
    def test_toggle_flag(self):
        """Test toggling flags."""
        board = Board(10, 10, 15)
        # Can flag unrevealed cells
        self.assertTrue(board.toggle_flag(0, 0))
        self.assertTrue(board.grid[0][0].is_flagged)
        
        # Can unflag flagged cells
        self.assertTrue(board.toggle_flag(0, 0))
        self.assertFalse(board.grid[0][0].is_flagged)
        
        # Can't flag revealed cells
        board.grid[0][0].is_revealed = True
        self.assertFalse(board.toggle_flag(0, 0))

if __name__ == '__main__':
    unittest.main()