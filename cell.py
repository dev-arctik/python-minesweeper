class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    
    def reveal(self):
        """Reveal this cell if it's not flagged."""
        if not self.is_flagged:
            self.is_revealed = True
            return True
        return False
    
    def toggle_flag(self):
        """Toggle the flag status of an unrevealed cell."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False
    
    def place_mine(self):
        """Place a mine in this cell."""
        self.is_mine = True
    
    def increment_adjacent(self):
        """Increment the adjacent mine counter."""
        self.adjacent_mines += 1
    
    def __str__(self):
        if self.is_flagged:
            return "F"
        if not self.is_revealed:
            return "■"
        if self.is_mine:
            return "X"
        if self.adjacent_mines == 0:
            return " "
        return str(self.adjacent_mines)