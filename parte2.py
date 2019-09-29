#UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL
#INSTITUTO DE INFORMÁTICA
#TRABALHO DA DISCIPLINA INF01030 - FUNDAMENTOS DE VISÃO COMPUTACIONAL
#Implementa̧c̃ao de algoritmo de calibra̧c̃ao de câmera
#Alunos:  Leonardo Oliveira Wellausen
#Matheus Fernandes Kovaleski
#Orientadore:  Prof.  Dr.  Cĺaudio Rosito Jung

import cv2   # biblioteca opencv utilizada para funções de imagem
import numpy as np  # biblioteca numpy para funções matemáticas, como a SDV


# função que projeta um ponto do plano 3d do campo (coord homo) para o plano 2d de imagem utilizando a matriz mat, já realizando divisão perspectiva
def project(mat, arr):
    res = np.zeros((3, 1))
    for i in range(3):
        for j in range(3):
            res[i] += mat[i][j] * arr[j]
    res = res / res[2]
    for i in range(3):
        res[i] = np.round(res[i])
    return res


#  função que projeta um ponto 2d em coordenadas de tela para um ponto 3d (no plano z=0 do campo) no mundo
#  basicamente uma multiplicação matricial com divisão perspectiva
def reproject(mat, arr):
    res = np.zeros((3, 1))
    arr2 = [arr[0], arr[1], 1.0]
    for i in range(3):
        for j in range(3):
            res[i] += mat[i][j]*arr2[j]
    res = res / res[2]
    return res


#  função que desenha um quadrado vermelho na posição pos da imagem original
def draw_square_at(pos):
    global img
    img[int(pos[1]) - 2:int(pos[1]) + 2, int(pos[0]) - 2:int(pos[0]) + 2] = [0, 0, 255]


#  função que desenha uma linha (segmento de reta) de cor aleatória entre os pontos x1 e x2 na imagem original
def draw_line(x1, x2):
    global img
    img = cv2.line(img, x1, x2, (0, 0, 255), 2)


# função callback chamada quando é detectado um clique de mouse, desenha o jogador na tela
def mouse_callback(event, x, y, flags, params):
    if event == 1:
        #  é a posição onde o usuário clicou na tela
        pos = (x, y)

        #  projeção do ponto pos no plano da imagem para o plano 3d do campo
        point_plane3d = reproject(p_inv, pos)

        #  intersecções de uma linha paralela à linha de fundo (eixo x) que passa pelo ponto point_plane 3d
        #       com as duas linhas laterais do campo, determinando ponto de início e fim do seg de reta a ser desenhado
        #  intersecção são calculadas com base na distância em x das linhas laterais, que são conhecidaa, e na distância
        #       em y do ponto selecionado pelo usuário. de certa forma é um projeção do vetor point_plane3d nas retas
        #       x=lat1 e x=lat2
        int_point1 = (lat1, point_plane3d[1], 1.0)
        int_point2 = (lat2, point_plane3d[1], 1.0)

        #  os pontos de intersecção encontrados são então projetados ao plano de imagem
        int_point12d = project(p_matrix, int_point1)
        int_point22d = project(p_matrix, int_point2)

        #  e por último desenhamos o segmento de reta ligando os dois pontos de intersecção
        draw_line((int_point12d[0], int_point12d[1]), (int_point22d[0], int_point22d[1]))

        #  exibimos a imagem atualizada
        cv2.imshow('image', img)


# carregamos a imagem, dimensionamos uma janela para exibí-la, setamos a função de callback definida anteriormente
img = cv2.imread('maracana2.jpg')
size = (img.shape[1], img.shape[0])
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', size[0], size[1])
cv2.setMouseCallback('image', mouse_callback)

# pontos medidos manualmente que serão utilizados para a calibração da câmera
# dicionário onde a chave é uma tupla 2d de coordenadas de pixel e seus valores são os correspondentes pontos 3d (coord homo) representando o ponto no mundo
points = {
    (589, 116): (0.0, 0.0, 1.0),
    (269, 62): (16.5, 16.5, 1.0),
    (474, 100): (5.5, 5.5, 1.0),
    (267, 238): (-23.82, 16.5, 1.0),
    (509, 177): (-12.82, 5.5, 1.0),
    (377, 134): (-3.66, 11.0, 1.0)
}
#  distâncias em x que definem as linhas laterais do campo
lat1 = 31.0
lat2 = -38.2

# estrutura que armezanará a matriz P de câmera
p_matrix = np.zeros((3, 3))

# dimensões da matriz de equações lineares
dima1 = len(points) * 2
dima2 = p_matrix.size

# matriz A de equações lineares que será a base para estimar P
a_matrix = np.zeros((dima1, dima2))

# preenchimento da matriz A de acordo com o slide 10 da aula 4
# utlizando os pontos definidos anteriormente e medidos manualmente
i = 0
keys = list(points.keys())
for k in range(dima1 // 2):
    point2d = keys[k]
    point3d = points[point2d]

    i = k * 2

    a_matrix[i][0] = point3d[0]
    a_matrix[i][1] = point3d[1]
    a_matrix[i][2] = 1.0
    a_matrix[i][3] = 0.0
    a_matrix[i][4] = 0.0
    a_matrix[i][5] = 0.0
    a_matrix[i][6] = -1 * point2d[0] * point3d[0]
    a_matrix[i][7] = -1 * point2d[0] * point3d[1]
    a_matrix[i][8] = -1 * point2d[0]

    i = i + 1

    a_matrix[i][0] = 0.0
    a_matrix[i][1] = 0.0
    a_matrix[i][2] = 0.0
    a_matrix[i][3] = point3d[0]
    a_matrix[i][4] = point3d[1]
    a_matrix[i][5] = 1.0
    a_matrix[i][6] = -1 * point2d[1] * point3d[0]
    a_matrix[i][7] = -1 * point2d[1] * point3d[1]
    a_matrix[i][8] = -1 * point2d[1]

# função numpy para o algoritmo de svd
# s é um array com os valores singulares ordenados de forma decrescente
# colunas de u são os autovetores de AA^t
# linhas de vh são os autovetores de A^tA, estando aqui o autovetor de interesse
# a = u diag(s) vh  onde diag(s) é uma matriz diagonal sendo o vetor s sua diagonal
u, s, vh = np.linalg.svd(a_matrix)

# o resultado do nosso sistema é o autovetor correspondente au menot valor singular de a
# como s é ordenado de forma decrescente, o menor valor singular é a última posição de s, correspondente na última linha de vh
# m é o solução para o nosso sisteminha a
m = vh[dima2 - 1, :]

# transformamos o array m da solução para o formato de matriz 3x4 de interesse
# p_matrix agora está devidamente ajustada e é a matriz de transformação de interesse!!
k = 0
for i in range(3):
    for j in range(3):
        p_matrix[i][j] = m[k]
        k += 1

#   calculamos a inversa da matriz p, essa matriz será utilizada pra a projeção de pontos no plano da imagem para o plano 3d do campo
p_inv = np.linalg.inv(p_matrix)

# exibimos a imagem por último para não receber cliques antes de tudo devidamente calculado
cv2.imshow('image', img)


# ficamos em laço esperando o usuário ou fechar a janela ou clicar na imagem (botão esquerdo) para adicionar um jogador
k = 0
while 1:
    k = cv2.waitKey(0)

    if k == 27:
        cv2.destroyAllWindows()
        break
