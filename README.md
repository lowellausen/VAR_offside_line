# VAR_offside_line

Single image camera calibration with DLT (direct linear transformation) method applied to a football field, using Python3 with OpenCV and numpy.

Goal of this project: given an image where we know the dimentions of the objects shown (in this case a football field, Maracanã, where all the distances are known) we 
want to calculate a projection matrix (related to that specific camera) that will map the real world 3D points to the 2D points in the image. The follwoing twoimages were used:   

![Alt text](maracana2.jpg?raw=true "Maracanã field") ![Alt text](maracana1.jpg?raw=true "Maracanã field")

How to do that: we manually map known points from the real world (based on dimensions and randomly taking one point as the origin to the coordinate system) and relate 
them to their also know pixel positions in the image; with that we can create a linear system (image_point = projection_matrix x realworld_point), solving that system 
by thw SVD (singular value decomposition) method we can get our projection matrix. The points selected, the goal on the left one is only to map the 2D plane that's the acutal field, whereas in the right one it is to map the whole 3D space therefore more points are needed to form the linear system:

![Alt text](relats/maracana2pontos.jpg?raw=true "Maracanã field") ![Alt text](relats/maracana1pontos.jpg?raw=true "Maracanã field")

Now we can use our projection matrix (and inverse) to project screen points to real world points, manipulate those points and then project back to screen.

In the image where we mapped the fiel plane only (z=0), the goal is to make an offside line just like the one shown. The user clicks somewhere in the screen, that point is projected to 3D, where where a straight line is made from side to side of the field, then projected to the image:

![Alt text](relats/res2.png?raw=true "Initial scene")

In the other image we map the 3D space, the goal is to project a "player". The user clicks somehwere in the screen. that point is projected to 3D (considering Z=0 hence the field plane), where a straight line is made from the point (x, y, 0) selected to (x, y, 1.8) to represent a player, then projected to the image:

(disclaimer: a bug may cause Neymar to show instead of a line sometimes)

![Alt text](relats/res1.png?raw=true "Initial scene")
