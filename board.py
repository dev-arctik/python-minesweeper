import random
import numpy as np
from cell import Cell

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = min(num_mines, width * height - 1)  # Ensure we don't have too many mines
        self.first_move_made = False
        self.game_over = False
        self.win = False
        
        # Initialize board with cells
        self.grid = np.array([[Cell() for _ in range(width)] for _ in range(height)])
    
    def place_mines(self, first_x, first_y):
        """Place mines randomly, ensuring first clicked cell is not a mine."""
        # Flatten the grid coordinates into a list of tuples
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # Remove the first click position and its adjacent cells
        safe_positions = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = first_x + dx, first_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_positions.append((nx, ny))
        
        # Filter out safe positions
        mine_candidates = [pos for pos in positions if pos not in safe_positions]
        
        # Randomly select mine positions
        mine_positions = random.sample(mine_candidates, self.num_mines)
        
        # Place mines and update adjacent counts
        for x, y in mine_positions:
            self.grid[y][x].place_mine()
            
            # Update adjacent cells
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not (dx == 0 and dy == 0):
                        self.grid[ny][nx].increment_adjacent()
    
    def reveal_cell(self, x, y):
        """Reveal a cell. If it's the first move, place mines first."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        # Handle first move
        if not self.first_move_made:
            self.place_mines(x, y)
            self.first_move_made = True
        
        cell = self.grid[y][x]
        
        # If already revealed or flagged, do nothing
        if cell.is_revealed or cell.is_flagged:
            return False
        
        # Reveal the cell
        cell.reveal()
        
        # Check if mine was hit
        if cell.is_mine:
            self.game_over = True
            return True
        
        # If empty cell (no adjacent mines), reveal adjacent cells recursively
        if cell.adjacent_mines == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not (dx == 0 and dy == 0):
                        self.reveal_cell(nx, ny)
        
        # Check for win condition
        self.check_win()
        
        return True
    
    def toggle_flag(self, x, y):
        """Toggle flag on a cell."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        return self.grid[y][x].toggle_flag()
    
    def chord(self, x, y):
        """
        Perform a chord action on a revealed number.
        If the number of adjacent flags matches the number in the cell,
        reveal all unflagged adjacent cells.
        Returns True if successful, False otherwise.
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        
        cell = self.grid[y][x]
        
        # Only chord on revealed numbers
        if not cell.is_revealed or cell.is_mine or cell.adjacent_mines == 0:
            return False
        
        # Count adjacent flags
        adjacent_flags = 0
        adjacent_cells = []
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and not (dx == 0 and dy == 0):
                    adjacent_cell = self.grid[ny][nx]
                    if adjacent_cell.is_flagged:
                        adjacent_flags += 1
                    else:
                        adjacent_cells.append((nx, ny))
        
        # If flags match the number, reveal all unflagged adjacent cells
        if adjacent_flags == cell.adjacent_mines:
            # Check for incorrect flags - if a flag is not on a mine, game over
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and not (dx == 0 and dy == 0):
                        adjacent_cell = self.grid[ny][nx]
                        if adjacent_cell.is_flagged and not adjacent_cell.is_mine:
                            # Incorrect flag found! Reveal and trigger game over
                            adjacent_cell.is_flagged = False
                            adjacent_cell.reveal()
                            self.game_over = True
                            return True
            
            # All flags are correct, reveal all unflagged adjacent cells
            for nx, ny in adjacent_cells:
                self.reveal_cell(nx, ny)
            
            return True
        
        return False
    
    def check_win(self):
        """Check if all non-mine cells are revealed."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                # If a non-mine cell is not revealed, game is not won yet
                if not cell.is_mine and not cell.is_revealed:
                    return False
        
        # All non-mine cells are revealed, game is won
        self.win = True
        return True
    
    def get_visible_board(self):
        """Return a 2D array representation of the visible board."""
        return [[str(self.grid[y][x]) for x in range(self.width)] for y in range(self.height)]
    
    def __str__(self):
        """String representation of the board for console display."""
        result = ""
        for y in range(self.height):
            result += " ".join(str(self.grid[y][x]) for x in range(self.width)) + "\n"
        return result