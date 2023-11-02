import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 1000
window_height = 1000

# Create the window
window = pygame.display.set_mode((window_width, window_height))

# Set the position of the jack o lantern
centerX = window_width / 2
centerY = window_height / 2

# Set the size of the jack o lantern
size = 200

# Set the colors of the jack o lantern
orange = (255, 165, 0)
black = (0, 0, 0)

# Set up mouse variables
mouseX = 0
mouseY = 0

def draw():
    # Draw the jack o lantern
    pygame.draw.circle(window, orange, (centerX, centerY), size)

    # draw the stem
    pygame.draw.rect(window, (0x34, 0x62, 0x2f), (centerX - 10, centerY - size - 40, 20, 80))
    pygame.draw.rect(window, (0x34, 0x62, 0x2f), (centerX - 10, centerY - size - 40, 80, 20))

    # draw the eyes
    eyeHeight = size / 4 + 50
    pygame.draw.polygon(window, black, ((centerX - size / 3, centerY - eyeHeight), (centerX - size / 3 - 40, centerY - eyeHeight + 70), (centerX - size / 3 + 40, centerY - eyeHeight + 70)))
    pygame.draw.polygon(window, black, ((centerX + size / 3, centerY - eyeHeight), (centerX + size / 3 + 40, centerY - eyeHeight + 70), (centerX + size / 3 - 40, centerY - eyeHeight + 70)))

    # draw the pupils
    pupilRadius = 20
    x = centerX - size / 3 + mouseX / 5
    pygame.draw.circle(window, (255, 255, 255), (x, centerY - eyeHeight / 2 + mouseY / 5), pupilRadius)
    pygame.draw.circle(window, (255, 255, 255), (centerX + size / 3 + mouseX / 5, centerY - eyeHeight / 2 + mouseY / 5), pupilRadius)

    # draw the nose
    pygame.draw.polygon(window, black, ((centerX, centerY - 30), (centerX - 25, centerY + 30), (centerX + 25, centerY + 30)))

    # draw the mouth
    pygame.draw.rect(window, black, (centerX - 100, centerY + 50, 201, 20))
    for i in range(0, 5):
        pygame.draw.polygon(window, black, ((centerX - 100 + (i * 40), centerY + 70), (centerX - 100 + (i * 40) + 20, centerY + 110), (centerX - 100 + (i * 40) + 40, centerY + 70)))

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Handle mouse movement
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
            print(mouseX, mouseY)

        # Clear the screen
        window.fill((0, 0, 0))

        draw()

    # Update the display
    pygame.display.update()