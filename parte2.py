

import urllib
import cv2
#from win32api import GetSystemMetrics

#the [x, y] for each right-click event will be stored here
left_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):

    #right-click event value is 2
    if event == 1:
        global left_clicks

        #store the coordinates of the right-click event
        left_clicks.append([x, y])

        #this just verifies that the mouse data is being collected
        #you probably want to remove this later
        print(left_clicks)

#path_image = urllib.urlretrieve("http://www.bellazon.com/main/uploads/monthly_06_2013/post-37737-0-06086500-1371727837.jpg", "local-filename.jpg")[0]
img = cv2.imread('maracana1.jpg')
scale_width = 640 / img.shape[1]
scale_height = 480 / img.shape[0]
scale = min(scale_width, scale_height)
window_width = int(img.shape[1] * scale)
window_height = int(img.shape[0] * scale)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', window_width, window_height)

#set mouse callback function for window
cv2.setMouseCallback('image', mouse_callback)

cv2.imshow('image', img)
cv2.waitKey(0)
##cv2.destroyAllWindows()
