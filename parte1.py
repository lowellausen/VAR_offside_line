import cv2
import numpy as np


def mouse_callback(event, x, y, flags, params):

    if event == 1:
        pos = (x, y)

        print(pos)


img = cv2.imread('maracana1.jpg')
size = (img.shape[1], img.shape[0])
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', size[0], size[1])
cv2.setMouseCallback('image', mouse_callback)


points = {
    (124, 156): (0.0, 0.0, 0.0),  #origem (trave esquerda com lina de fundo)
    (123, 126): (0.0, 0.0, 2.44),  #alto da trave esquerda
    (160, 175): (5.5, 5.5, 0.0),  #pequena area
    (154, 158): (-3.66, 11.0, 0.0),  #mara de penalti, talvez
    (159, 124): (-7.32, 0.0, 1.22),  #meio da trave direita
    (274, 83):  (-48.66, 0.0, 0.0),  #bandeira
    (249, 221): (16.5, 16.5, 0.0)    #grande area
     }
"""
origem = (124,156) #ponto(0,0,0)
trave = (123, 126)
altura_trave = 2.44
#ponto (0,0,altura_trave)
peq_area = (160,175) #ponto (5.5, 5.5, 0)
penalti = (254, 158)# ponto (-3.66 ,11.0,0.0)
trave_dir = (159,124)#(-7.32, 0, 1.22)
bandeira = (274,83)# (-48.66, 0,0)
grande_area = (249,221)#(16.5,16.5,0)
"""


############################################################################################
############## CALIBRATE DO OPENCV PARA TIRA TEIMAS ########################################


#preparando em arrays para a função opencv
world_points = []
img_points = []

for k in points.keys():
    world_points.append(tuple(points[k]))
    img_points.append(tuple(k))

world_points = np.array(world_points, 'float32')
img_points = np.array(img_points, 'float32')

camera_matrix = cv2.initCameraMatrix2D([world_points], [img_points], size)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([world_points], [img_points], size, camera_matrix, None, flags=cv2.CALIB_USE_INTRINSIC_GUESS)
rodri, jacobison = cv2.Rodrigues(rvecs[0])
concat = np.hstack((rodri, tvecs[0]))



##############################################################################################
##############################################################################################





cv2.imshow('image', img)


k = 0
#set mouse callback function for window
while 1:
    k = cv2.waitKey(0)

    if (k == 27):
        cv2.destroyAllWindows()
        break
