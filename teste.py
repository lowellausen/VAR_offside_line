import numpy as np


def project(mat, arr):
	res = np.zeros((3, 1))
	for i in range(3):
		for j in range(4):
			res[i] += mat[i][j]*arr[j]
	res = res/res[2]
	return res


points = {
	(124, 156): (0.0, 0.0, 0.0, 1.0),  # origem (trave esquerda com lina de fundo)
	(123, 126): (0.0, 0.0, 2.44, 1.0),  # alto da trave esquerda
	(160, 175): (5.5, 5.5, 0.0, 1.0),  # pequena area
	(154, 158): (-3.66, 11.0, 0.0),  # mara de penalti, talvez
	(159, 124): (-7.32, 0.0, 1.22),  # meio da trave direita
	(274, 83): (-48.66, 0.0, 0.0),  # bandeira
	#(249, 221): (16.5, 16.5, 0.0)  # grande area
}

m_matrix = np.zeros((3, 4))

dima1 = len(points) * 2
dima2 = m_matrix.size

a_matrix = np.zeros((dima1, dima2))

i = 0
keys = list(points.keys())
for k in range(dima1 // 2):
	point2d = keys[k]
	point3d = points[point2d]

	i = k * 2

	a_matrix[i][0] = point3d[0]
	a_matrix[i][1] = point3d[1]
	a_matrix[i][2] = point3d[2]
	a_matrix[i][3] = 1.0
	a_matrix[i][4] = 0.0
	a_matrix[i][5] = 0.0
	a_matrix[i][6] = 0.0
	a_matrix[i][7] = 0.0
	a_matrix[i][8] = -1 * point2d[0] * point3d[0]
	a_matrix[i][9] = -1 * point2d[0] * point3d[1]
	a_matrix[i][10] = -1 * point2d[0] * point3d[2]
	a_matrix[i][11] = -1 * point2d[0]

	i = i + 1

	a_matrix[i][0] = 0.0
	a_matrix[i][1] = 0.0
	a_matrix[i][2] = 0.0
	a_matrix[i][3] = 0.0
	a_matrix[i][4] = point3d[0]
	a_matrix[i][5] = point3d[1]
	a_matrix[i][6] = point3d[2]
	a_matrix[i][7] = 1.0
	a_matrix[i][8] = -1 * point2d[1] * point3d[0]
	a_matrix[i][9] = -1 * point2d[1] * point3d[1]
	a_matrix[i][10] = -1 * point2d[1] * point3d[2]
	a_matrix[i][11] = -1 * point2d[1]

u, s, vh = np.linalg.svd(a_matrix)

m = vh[dima2-1,:]
k = 0

for i in range(3):
	for j in range(4):
		m_matrix[i][j] = m[k]
		k += 1

print(mult(m_matrix,points[keys[0]]))

for i in range(dima1):
	for j in range(dima2):
		print(str(a_matrix[i][j]) + '\t', end='')
	print('\n')
