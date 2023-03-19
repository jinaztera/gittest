import pygame
import random

# Initialize pygame
pygame.init()

# Set the window size and title
window_size = (500, 700)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tetris")

# Define block size and margin
block_size = 25
margin = 5

# Define the Tetromino shapes
T = [['.....',
      '..O..',
      '.OOO.',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..'],
     ['.....',
      '.O...',
      '.OO..',
      '..O..']]

# Define the initial values
current_piece = T
color = (255, 0, 0)
x = int(window_size[0] / 2 - block_size * 2)
y = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        # Handle quitting
        if event.type == pygame.QUIT:
            running = False

        # Handle key events for moving the piece
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= block_size
            if event.key == pygame.K_RIGHT:
                x += block_size
            if event.key == pygame.K_UP:
                current_piece = [list(x[::-1]) for x in zip(*current_piece[::-1])]
            if event.key == pygame.K_DOWN:
                y += block_size

    # Draw the current piece on the screen
    for row in range(len(current_piece)):
        for col in range(len(current_piece[row])):
            if current_piece[row][col] == 'O':
                pygame.draw.rect(window, color, (x + col * block_size, y + row * block_size, block_size - margin, block_size - margin))

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()
