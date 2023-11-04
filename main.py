import pygame
import math
import cv2

# Load the cascade for detecting faces and initialize the webcam
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

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
# mouthClosedImg = pygame.image.load('jack-o-lantern.png')
# mouthClosedImg = pygame.transform.scale(mouthClosedImg, (size, size))

# mouthOpenImg = pygame.image.load('jack-o-lantern-mouth-open.png')
# mouthOpenImg = pygame.transform.scale(mouthOpenImg, (size, size))

headImg = pygame.image.load('head.png')
headImg = pygame.transform.scale(headImg, (size, 400))

jawImg = pygame.image.load('jaw.png')
jawImg = pygame.transform.scale(jawImg, (510, size / 2))

# Set the colors of the jack o lantern
orange = (255, 165, 0)
black = (0, 0, 0)

def draw(prevDistX=0, prevDistY=0, jawDeltaY=0):
    # Clear the window
    window.fill((0x10, 0x10, 0x13))

    # Draw the eyes
    eyeSize = 60
    eyeColor = (0x41, 0x1c, 0x09)
    pupilSize = 20
    pupilColor = (0xfe, 0xff, 0)

    def drawEye(eyeX, eyeY, distX, distY):
        # distX = mouseX - eyeX
        # distY = mouseY - eyeY
        dist = min(math.sqrt((distX) ** 2 + (distY) ** 2), 20)
        angle = math.atan2(distY, distX)
        pupilX = eyeX + (math.cos(angle) * dist)
        pupilY = eyeY + (math.sin(angle) * dist)

        pygame.draw.circle(window, pupilColor, (pupilX, pupilY), pupilSize)

    def findFace():
        ret, frame = cap.read()
        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.5, 5)

        try:
            (x, y, w, h) = faces[0]
        except IndexError:
            return None
        height, width, channels = frame.shape

        distX = x + w / 2 - width / 2
        distY = y + h / 2 - height / 2

        return -distX, distY
    
    dists = findFace()
    if dists is None:
        dists = (prevDistX, prevDistY)
    distX, distY = dists
    prevDistX, prevDistY = distX, distY

    # Left eye
    pygame.draw.circle(window, eyeColor, (centerX - size / 5, centerY + 10), eyeSize)
    drawEye(centerX - size / 5, centerY + 10, distX, distY)

    # Right eye
    pygame.draw.circle(window, eyeColor, (centerX + size / 5, centerY + 10), eyeSize)
    drawEye(centerX + size / 5, centerY + 10, distX, distY)

    
    window.blit(headImg , (255, 240))
    window.blit(jawImg , (248, 490 + jawDeltaY))
    # window.blit(jawImg , (248, 550 + jawDeltaY))

# Main game loop
jawDeltaY = 0
opening = True
talking = False
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    prevDistX, prevDistY = 0, 0
    draw(prevDistX=prevDistX, prevDistY=prevDistY, jawDeltaY=jawDeltaY)

    if talking:
        if jawDeltaY == 60:
            opening = False
        elif jawDeltaY == 0:
            opening = True
        
        if opening:
            jawDeltaY += 15
        else:
            jawDeltaY -= 15
    
    # Update the display
    pygame.display.update()