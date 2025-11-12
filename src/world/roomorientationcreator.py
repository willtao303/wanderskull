import numpy
import cv2
white = [255, 255, 255]
grey = [210, 210, 210]
red = [30, 30, 243]
green = [30, 243, 30]
black = [40, 40, 40]
def set_tile(img, n):
    x = (n % 16)*5 + 1
    y = (n // 16)*5 + 1

    col = green

    peices = [[(n & 1), ((n >> 1) & 1), ((n >> 2) & 1)],
              [((n >> 7) & 1), None, ((n >> 3) & 1)],
              [((n >> 6) & 1), ((n >> 5) & 1), ((n >> 4) & 1)]]
    
    if (peices[0][0]):
        if not (peices[0][1] and peices[1][0]):
            col = red
    if (peices[0][2]):
        if not (peices[1][2] and peices[0][1]):
            col = red
    if (peices[2][0]):
        if not (peices[2][1] and peices[1][0]):
            col = red
    if (peices[2][2]):
        if not (peices[2][1] and peices[1][2]):
            col = red

    for i in range(5):
        for j in range(5):
            if ((n % 16) % 2) ^ ((n // 16) % 2):
                img[y - 1 + j][x - 1 + i] = white
            else: 
                img[y - 1 + j][x - 1 + i] = grey

    for i in range(3):
        for j in range(3):
            if (peices[j][i] == None):
                img[y + j][x + i] = black
            elif (peices[j][i]):
                img[y + j][x + i] = col

img_path = "src/world/tile_orientations.png"
img = cv2.imread(img_path, cv2.IMREAD_COLOR_RGB )
for i in range(256):
    set_tile(img, i)
cv2.imshow("Image", img)
cv2.imwrite(img_path, img)
cv2.waitKey(0)
cv2.destroyAllWindows()
