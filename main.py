# main.py
import pygame
import sys
import time
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
    
    # Variables for tracking game time
    start_time = time.time()
    game_time = 0
    last_time_update = 0
    timer_paused = False
    
    # Flag to track when we need to redraw the board
    need_board_update = True
    
    try:
        running = True
        while running:
            current_time = time.time()
            
            # Update game time only once per second to avoid flickering
            # and only if the game is not over
            if not timer_paused and int(current_time - start_time) > last_time_update:
                game_time = current_time - start_time
                last_time_update = int(game_time)
                
                # Draw the stats
                renderer.draw_stats(
                    game.get_flags_remaining(),
                    game.flags_used,
                    game_time
                )
                pygame.display.update(pygame.Rect(0, 0, renderer.screen_width, renderer.stats_height))
            
            # Check if game is over and pause timer if needed
            if (game.is_game_over() or game.is_win()) and not timer_paused:
                timer_paused = True
                # Make sure stats are updated one last time with final time
                renderer.draw_stats(
                    game.get_flags_remaining(),
                    game.flags_used,
                    game_time
                )
                pygame.display.update(pygame.Rect(0, 0, renderer.screen_width, renderer.stats_height))
            
            # Process events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Get the position of the click
                    pos = pygame.mouse.get_pos()
                    cell_pos = renderer.get_cell_at_pos(pos)
                    
                    if cell_pos:
                        x, y = cell_pos
                        
                        # Left click - reveal cell or chord
                        if event.button == 1:
                            if game.is_game_over() or game.is_win():
                                # Restart the game
                                game.new_game()
                                start_time = time.time()
                                game_time = 0
                                last_time_update = 0
                                timer_paused = False
                            else:
                                # Get the board state to check if we're clicking on a revealed number
                                board_state = game.get_board_state()
                                try:
                                    cell_value = board_state[y][x]
                                    # If it's a revealed number, try to chord
                                    if cell_value not in ["■", "F", "X", " "]:
                                        game.chord(x, y)
                                    else:
                                        # Otherwise, just reveal the cell
                                        game.reveal_cell(x, y)
                                except (IndexError, ValueError):
                                    # If there's any error, just do a normal reveal
                                    game.reveal_cell(x, y)
                            
                            need_board_update = True
                        
                        # Right click - toggle flag
                        elif event.button == 3:
                            if not (game.is_game_over() or game.is_win()):
                                game.toggle_flag(x, y)
                                need_board_update = True
                                
                                # Update stats display immediately after flagging
                                renderer.draw_stats(
                                    game.get_flags_remaining(),
                                    game.flags_used,
                                    game_time
                                )
                                pygame.display.update(pygame.Rect(0, 0, renderer.screen_width, renderer.stats_height))
            
            # Only redraw the board when needed (on init and after events)
            if need_board_update:
                # If game over, ensure we reveal all mines for proper rendering
                if game.is_game_over():
                    # Make sure all mines are revealed in the board display
                    for y in range(game.height):
                        for x in range(game.width):
                            cell = game.board.grid[y][x]
                            if cell.is_mine:
                                cell.is_revealed = True
                
                renderer.draw_board(
                    game.get_board_state(),
                    game.is_game_over(),
                    game.is_win()
                )
                pygame.display.update(pygame.Rect(
                    0, renderer.stats_height, 
                    renderer.screen_width, renderer.height * renderer.cell_size
                ))
                need_board_update = False
            
            # Cap the frame rate
            pygame.time.Clock().tick(30)
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        renderer.cleanup()
        sys.exit()

if __name__ == "__main__":
    main()