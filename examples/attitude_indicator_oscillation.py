import sys
import pygame
from math import sin, cos
import time
from flight_instruments import AttitudeIndicator


if __name__ == '__main__':
        
    # Initialize Pygame
    pygame.init()

    # Define the width and height of the window
    width, height = 700, 700

    # Create a Pygame window
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Attitude Indicator")

    # Main loop
    running = True

    ai = AttitudeIndicator(width=width, height=height)

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(ai.get_screen(row_deg= 2 * sin(0.5*time.time()), pitch_deg = 10 * cos(time.time())), (0,0))
        
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()