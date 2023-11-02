import pygame
import math

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
size = 500

# Load the image
image = pygame.image.load('jack-o-lantern.png')
image = pygame.transform.scale(image, (size, size))

# Set the colors of the jack o lantern
orange = (255, 165, 0)
black = (0, 0, 0)

def draw():
    # Clear the window
    window.fill(black)

    window.blit(image, (centerX - size / 2, centerY - size / 2))

    # Draw the eyes
    eyeSize = 40
    eyeColor = (255, 255, 255)
    pupilSize = 20
    pupilColor = (0, 0, 100)

    mouseX, mouseY = pygame.mouse.get_pos()
    def drawEye(eyeX, eyeY, mouseX, mouseY):
        distX = mouseX - eyeX
        distY = mouseY - eyeY
        dist = min(math.sqrt((distX) ** 2 + (distY) ** 2), 20)
        angle = math.atan2(distY, distX)
        pupilX = eyeX + (math.cos(angle) * dist)
        pupilY = eyeY + (math.sin(angle) * dist)

        pygame.draw.circle(window, pupilColor, (pupilX, pupilY), pupilSize)
    
    mouseX, mouseY = pygame.mouse.get_pos()

    # Left eye
    pygame.draw.circle(window, eyeColor, (centerX - size / 5, centerY + 10), eyeSize)
    drawEye(centerX - size / 5, centerY + 10, mouseX, mouseY)

    # Right eye
    pygame.draw.circle(window, eyeColor, (centerX + size / 5, centerY + 10), eyeSize)
    drawEye(centerX + size / 5, centerY + 10, mouseX, mouseY)


# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    draw()

    # Update the display
    pygame.display.update()