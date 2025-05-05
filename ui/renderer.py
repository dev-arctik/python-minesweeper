# ui/renderer.py
import pygame
import pygame.font

class GameRenderer:
    # Colors
    GRID_COLOR = (128, 128, 128)
    CELL_COLOR = (200, 200, 200)
    REVEALED_COLOR = (180, 180, 180)
    MINE_COLOR = (255, 0, 0)
    FLAG_COLOR = (255, 165, 0)
    TEXT_COLORS = {
        1: (0, 0, 255),      # Blue
        2: (0, 128, 0),      # Green
        3: (255, 0, 0),      # Red
        4: (0, 0, 128),      # Dark Blue
        5: (128, 0, 0),      # Dark Red
        6: (0, 128, 128),    # Teal
        7: (0, 0, 0),        # Black
        8: (128, 128, 128)   # Gray
    }
    
    def __init__(self, width, height, cell_size=30, stats_height=40):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.stats_height = stats_height
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size + stats_height
        
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Minesweeper")
        
        # Initialize fonts
        self.font = pygame.font.SysFont('Arial', cell_size // 2)
        self.stats_font = pygame.font.SysFont('Arial', 18)
    
    def draw_board(self, board_state, game_over=False, win=False):
        """Draw the board based on its current state."""
        # Fill the board area only (not the stats bar)
        board_area = pygame.Rect(0, self.stats_height, self.screen_width, self.height * self.cell_size)
        self.screen.fill((255, 255, 255), board_area)
        
        for y in range(self.height):
            for x in range(self.width):
                cell = board_state[y][x]
                rect = pygame.Rect(
                    x * self.cell_size, 
                    y * self.cell_size + self.stats_height,  # Offset for stats bar
                    self.cell_size, 
                    self.cell_size
                )
                
                # Draw cell background
                if cell == "■":  # Unrevealed
                    pygame.draw.rect(self.screen, self.CELL_COLOR, rect)
                elif cell == "F":  # Flagged
                    pygame.draw.rect(self.screen, self.CELL_COLOR, rect)
                    flag_rect = pygame.Rect(
                        x * self.cell_size + self.cell_size // 4,
                        y * self.cell_size + self.stats_height + self.cell_size // 4,
                        self.cell_size // 2,
                        self.cell_size // 2
                    )
                    pygame.draw.rect(self.screen, self.FLAG_COLOR, flag_rect)
                elif cell == "X":  # Mine
                    pygame.draw.rect(self.screen, self.REVEALED_COLOR, rect)
                    mine_rect = pygame.Rect(
                        x * self.cell_size + self.cell_size // 4,
                        y * self.cell_size + self.stats_height + self.cell_size // 4,
                        self.cell_size // 2,
                        self.cell_size // 2
                    )
                    pygame.draw.rect(self.screen, self.MINE_COLOR, mine_rect)
                else:  # Revealed with number or empty
                    pygame.draw.rect(self.screen, self.REVEALED_COLOR, rect)
                    if cell != " ":  # Has adjacent mines
                        num = int(cell)
                        text = self.font.render(cell, True, self.TEXT_COLORS.get(num, (0, 0, 0)))
                        text_rect = text.get_rect(center=(
                            x * self.cell_size + self.cell_size // 2,
                            y * self.cell_size + self.stats_height + self.cell_size // 2
                        ))
                        self.screen.blit(text, text_rect)
                
                # Draw cell border
                pygame.draw.rect(self.screen, self.GRID_COLOR, rect, 1)
        
        # Draw game over or win message
        if game_over or win:
            overlay = pygame.Surface((self.screen_width, self.height * self.cell_size), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 128))  # Semi-transparent white
            self.screen.blit(overlay, (0, self.stats_height))
            
            if game_over:
                message = "Game Over! Click to restart."
            else:  # win
                message = "You Win! Click to restart."
            
            text = pygame.font.SysFont('Arial', 32).render(message, True, (0, 0, 0))
            text_rect = text.get_rect(center=(
                self.screen_width // 2, 
                self.stats_height + (self.height * self.cell_size) // 2
            ))
            self.screen.blit(text, text_rect)
    
    def draw_stats(self, mines_remaining, flags_used, game_time):
        """Draw simple game statistics at the top."""
        # Draw stats background
        stats_rect = pygame.Rect(0, 0, self.screen_width, self.stats_height)
        pygame.draw.rect(self.screen, (220, 220, 220), stats_rect)
        pygame.draw.line(self.screen, (180, 180, 180), 
                        (0, self.stats_height), 
                        (self.screen_width, self.stats_height), 2)
        
        # Format the time as MM:SS
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Draw the stats
        mines_text = self.stats_font.render(f"Mines: {mines_remaining}", True, (0, 0, 0))
        flags_text = self.stats_font.render(f"Flags: {flags_used}", True, (0, 0, 0))
        time_text = self.stats_font.render(f"Time: {time_str}", True, (0, 0, 0))
        
        padding = 20
        mines_rect = mines_text.get_rect(midleft=(padding, self.stats_height // 2))
        flags_rect = flags_text.get_rect(center=(self.screen_width // 2, self.stats_height // 2))
        time_rect = time_text.get_rect(midright=(self.screen_width - padding, self.stats_height // 2))
        
        self.screen.blit(mines_text, mines_rect)
        self.screen.blit(flags_text, flags_rect)
        self.screen.blit(time_text, time_rect)
    
    def get_cell_at_pos(self, pos):
        """Convert screen position to board coordinates."""
        x, y = pos
        board_x = x // self.cell_size
        board_y = (y - self.stats_height) // self.cell_size
        
        if 0 <= board_x < self.width and 0 <= board_y < self.height:
            return board_x, board_y
        return None
    
    def cleanup(self):
        """Clean up pygame resources."""
        pygame.quit()