#UNIVERSIDADE FEDERAL DO RIO GRANDE DO SUL
#INSTITUTO DE INFORMÁTICA
#TRABALHO DA DISCIPLINA INF01030 - FUNDAMENTOS DE VISÃO COMPUTACIONAL
#Implementa̧c̃ao de algoritmo de calibra̧c̃ao de câmera
#Alunos:  Leonardo Oliveira Wellausen
#Matheus Fernandes Kovaleski
#Orientadore:  Prof.  Dr.  Cĺaudio Rosito Jung

import cv2   # biblioteca opencv utilizada para funções de imagem
import numpy as np  # biblioteca numpy para funções matemáticas, como a SDV
from random import randint, choice  # random para escolha de cores e neys
import os


#  função que projeta o ponto 3d arr (coord homo) para o plano 2d de imagem utilizando a matriz mat, já realizando divisão perspectiva
#  basicamente uma multiplicação matricial com divisão perspectiva
def project(mat, arr):
    res = np.zeros((3, 1))
    for i in range(3):
        for j in range(4):
            res[i] += mat[i][j] * arr[j]
    res = res / res[2]
    for i in range(3):
        res[i] = np.round(res[i])
    return res


#  função que projeta um ponto 2d em coordenadas de tela para um ponto 3d (no plano z=0 do campo) no mundo
#  basicamente uma multiplicação matricial com divisão perspectiva
def reproject(mat, arr):
    res = np.zeros((4, 1))
    arr2 = [arr[0], arr[1], 1.0]
    for i in range(3):
        for j in range(3):
            res[i] += mat[i][j]*arr2[j]
    res = [res[0][0]/res[2][0], res[1][0]/res[2][0], 0.0, res[2][0]/res[2][0]]
    return res


#  função que desenha um quadrado vermelho na posição pos da imagem original
def draw_square_at(pos):
    global img
    img[int(pos[1]) - 2:int(pos[1]) + 2, int(pos[0]) - 2:int(pos[0]) + 2] = [0, 0, 255]


#  função que desenha uma linha (segmento de reta) de cor aleatória entre os pontos x1 e x2 na imagem original
def draw_line(x1, x2):
    global img
    img = cv2.line(img, x1, x2, (randint(0, 255), randint(0, 255), randint(0, 255)), 2)


#  função que desenha um neymar aleatório (dentre os disponíveis na base de dados em ./ney/) entre a posição x1 e x2 na imagem original
def draw_ney(x1, x2):
    ney = choice(os.listdir("./ney/"))
    newsize = (20, int(np.abs(x2[1] - x1[1]))+10)
    y_offset = int(x2[1] - newsize[1]/2)
    x_offset = int(x2[0] - newsize[0]/2)
    neyney = cv2.imread('./ney/' + ney, -1)
    neyney = cv2.resize(neyney, newsize,  interpolation=cv2.INTER_AREA)

    y1, y2 = y_offset, y_offset + neyney.shape[0]
    x1, x2 = x_offset, x_offset + neyney.shape[1]

    alpha_s = neyney[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        img[y1:y2, x1:x2, c] = (alpha_s * neyney[:, :, c] +
                                alpha_l * img[y1:y2, x1:x2, c])


# função callback chamada quando é detectado um clique de mouse, desenha o jogador na tela
def mouse_callback(event, x, y, flags, params):
    if event == 1 or event == 2:
        #  é a posição onde o usuário clicou na tela
        pos = (x, y)

        #  point_plane é a projeção do ponto de tela pos no plano 3d z=0 do campo, representado pés de um jogador
        point_plane = reproject(minip_inv, pos)
        #  incrementamos em 1.8 a coordenada z deste ponto no mundo, representado a altura do jogador
        point_plane[2] = 1.8
        #  e então projetamos este ponto 3d alterado de volta para o plano de imagem, em head_point2d, representando a cabeça de m jogador
        head_point2d = project(p_matrix, point_plane)

        #draw_square_at(pos)
        #draw_square_at(head_point2d)

        #  tendo os dois pontos do jogador em mãos (pés e cabeça) em coord de imagem podemos desenhar um segmento de reta os ligando, repesentando um jogador inteiro
        #  caso clique com botão esquerdo do mouse desenhamos o seg de reta, caso botão direito desenhamos um neymar
        if event == 1:
            draw_line((pos[0], pos[1]), (head_point2d[0], head_point2d[1]))
        else:
            draw_ney(np.asarray((pos[0], pos[1])), np.asarray((head_point2d[0][0], head_point2d[1][0])))

        #  atualiza a exibição da imagem
        cv2.imshow('image', img)


# carregamos a imagem, dimensionamos uma janela para exibí-la, setamos a função de callback definida anteriormente
img = cv2.imread('maracana1.jpg')
size = (img.shape[1], img.shape[0])
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', size[0], size[1])
cv2.setMouseCallback('image', mouse_callback)

# pontos medidos manualmente que serão utilizados para a calibração da câmera
# dicionário onde a chave é uma tupla 2d de coordenadas de pixel e seus valores são os correspondentes pontos 3d (coord homo) representando o ponto no mundo
points = {
    (124, 157): (0.0, 0.0, 0.0, 1.0),  # origem - inferior trave esquerda
    (161, 176): (5.5, 5.5, 0.0, 1.0),  # corner esquerdo pequena área
    (123, 127): (0.0, 0.0, 2.44, 1.0),  # gaveta trave esquerda
    (160, 139): (-7.32, 0.0, 0.0, 1.0),  # inferior trave direita
    (242, 131): (-12.82, 5.5, 0.0, 1.0),  # corner direito pequena área
    (159, 111): (-7.32, 0.0, 2.44, 1.0),  #gaveta trave direita
    (30, 204): (16.5, 0.0, 0.0, 1.0),  # corner linha de fundo grande área esquerda
    (227, 105): (-23.82, 0.0, 0.0, 1.0),  # corner linha de fundo grande área direita
    (252, 157): (-3.66, 11.0, 0.0, 1.0)  # marca de penal
}


# estrutura que armezanará a matriz P de câmera
p_matrix = np.zeros((3, 4))

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
    for j in range(4):
        p_matrix[i][j] = m[k]
        k += 1

#  para realizar a projeção inversa (coord de img para mundo) geramos uma versão mini da matriz p
#  onde mini significa sem os valores relativos ao eixo z do mundo; sem a terceira coluna
minip = np.zeros((3, 3))
for i in range(3):
    for j in range(4):
        if j == 2:
            continue
        minip[i][min(j, 2)] = p_matrix[i][j]

#  então calculamos a inversa de minip, essa matriz que será então usada para projeção de img para mundo
minip_inv = np.linalg.inv(minip)

# exibimos a imagem por último para não receber cliques antes de tudo devidamente calculado
cv2.imshow('image', img)

# ficamos em laço esperando o usuário ou fechar a janela ou clicar na imagem (botão esquerdo) para adicionar um jogador
k = 0
while 1:
    k = cv2.waitKey(0)

    saida = cv2.destroyAllWindows()
    if (saida == None):
        break
print(saida)
