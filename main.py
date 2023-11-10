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

def draw(prevDistX=0, prevDistY=0, faceX=0, faceY=0, jawDeltaY=0):
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
        
        pupilX = eyeX + max(min(distX * pupilMovementScale, 20), -20)
        pupilY = eyeY + max(min(distY * pupilMovementScale, 20), -20)

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
     
    faceDists = findFace()
    if faceDists is None:
        faceDists = (0, 0)

    faceX, faceY = faceDists

    # Left eye
    pygame.draw.circle(window, eyeColor, (centerX - size / 5, centerY + 10), eyeSize)
    drawEye(centerX - size / 5, centerY + 10, prevDistX, prevDistY)

    # Right eye
    pygame.draw.circle(window, eyeColor, (centerX + size / 5, centerY + 10), eyeSize)
    drawEye(centerX + size / 5, centerY + 10, prevDistX, prevDistY)

    
    window.blit(headImg , (255, 240))
    window.blit(jawImg , (248, 490 + jawDeltaY))
    # window.blit(jawImg , (248, 550 + jawDeltaY))

    return prevDistX, prevDistY, faceX, faceY

# Main game loop
jawDeltaY = 0
opening = True
talking = False

pupilMovementScale = 0.20 # Speed of the pupil movement
pupilFollowDeadzone = 2
pupilReturnDeadzone = 5
pupilMoveStep = 5 # How much the pupil moves every frame

prevDistX, prevDistY = 0, 0
faceX, faceY = 0, 0

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # If the eyes outside of the ceneter deadzone and there is no face, move them back by a step every frame then lock them at 0
    if faceX == 0 and faceY == 0:
        if abs(prevDistX) > pupilReturnDeadzone: prevDistX += pupilMoveStep if prevDistX < 0 else -pupilMoveStep
        else: prevDistX = 0
        
        if abs(prevDistY) > pupilReturnDeadzone: prevDistY += pupilMoveStep if prevDistY < 0 else -pupilMoveStep
        else: prevDistY = 0

    # If the eyes are currently not within the deadzone around the face, move them towards the face
    if prevDistX < faceX - pupilFollowDeadzone: prevDistX += pupilMoveStep 
    elif prevDistX > faceX + pupilFollowDeadzone: prevDistX -= pupilMoveStep
    if prevDistY < faceY - pupilFollowDeadzone: prevDistY += pupilMoveStep 
    elif prevDistY > faceY + pupilFollowDeadzone: prevDistY -= pupilMoveStep

    prevDistX, prevDistY, faceX, faceY = draw(prevDistX=prevDistX, prevDistY=prevDistY, faceX=faceX, faceY=faceY, jawDeltaY=jawDeltaY)

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