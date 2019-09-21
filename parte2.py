import cv2


def mouse_callback(event, x, y, flags, params):

    if event == 1:
        pos = (x, y)

        print(pos)
img = cv2.imread('maracana1.jpg')
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', img.shape[1], img.shape[0])

k = 0
#set mouse callback function for window
while 1:
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow('image', img)
    k = cv2.waitKey(0)

    if (k == 27):
        breakcv2.destroyAllWindows()
