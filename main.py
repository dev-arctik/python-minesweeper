import pygame
import sys
from game import MinesweeperGame
from ui.renderer import GameRenderer

def main():
    # Game parameters
    width = 10
    height = 10
    num_mines = 15
    cell_size = 40
    
    # Initialize game and renderer
    game = MinesweeperGame(width, height, num_mines)
    renderer = GameRenderer(width, height, cell_size)
    
    try:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the click
                    pos = pygame.mouse.get_pos()
                    cell_pos = renderer.get_cell_at_pos(pos)
                    
                    if cell_pos:
                        x, y = cell_pos
                        
                        # Left click - reveal cell
                        if event.button == 1:
                            if game.is_game_over() or game.is_win():
                                # Restart the game if it's over
                                game.new_game()
                            else:
                                game.reveal_cell(x, y)
                        
                        # Right click - toggle flag
                        elif event.button == 3:
                            if not (game.is_game_over() or game.is_win()):
                                game.toggle_flag(x, y)
            
            # Draw the current state of the board
            renderer.draw_board(
                game.get_board_state(),
                game.is_game_over(),
                game.is_win()
            )
            
            # Cap the frame rate
            pygame.time.Clock().tick(60)
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        renderer.cleanup()
        sys.exit()

if __name__ == "__main__":
    main()