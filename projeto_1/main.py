#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#===============================================================================

from multiprocessing.managers import BaseListProxy
import sys
import timeit
import numpy as np
import cv2
from imprime import imprime

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = True
THRESHOLD = 0.7
ALTURA_MIN = 15
LARGURA_MIN = 15
N_PIXELS_MIN = 500

#===============================================================================

def binariza(img, threshold):
    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    binary_img = np.where(img < threshold, 0, 1)
    # CHECKME: verificar com o professor se podemos retornar com uint8 mesmo, pois so assim deu pra exibir com a imgshow 
    return binary_img.astype(np.uint8)

#-------------------------------------------------------------------------------

img = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 0, 1, 0],
    [0, 0, 1, 1, 0],
]

def rotula(img, largura_min, altura_min, n_pixels_min):
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo(dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    largura = len(img[0])
    altura = len(img)
    rotulo = 2

    for i in range(0, altura):
        for j in range(0, largura):
            if img[i][j] == 1:
                inunda(rotulo, i, j)
                rotulo = rotulo + 1

    imprime(img, "INUNDADA")

#===============================================================================

def inunda(rotulo, y, x):
    largura = len(img[0])
    altura = len(img)

    if img[y][x] != 1:
        return

    img[y][x] = rotulo

    # Vizinho de cima
    if y > 0:
        inunda(rotulo, y - 1, x)
    # Vizinho de baixo
    if y < altura - 1:
        inunda(rotulo, y + 1, x)
    # Vizinho da esquerda
    if x > 0:
        inunda(rotulo, y, x - 1)
    # Vizinho da direita
    if x < largura - 1:
        inunda(rotulo, y, x + 1)


#===============================================================================

def main():
    # Abre a imagem em escala de cinza.
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape((img.shape[0], img.shape[1], 1))
    img = img.astype(np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza(img, THRESHOLD)
    cv2.imshow('01 - binarizada', img)
    cv2.imwrite('01 - binarizada.png', img*255)

    start_time = timeit.default_timer()
    componentes = rotula(img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len(componentes)
    print('Tempo: %f' %(timeit.default_timer() - start_time))
    print('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle(img_out,(c['L'], c['T']),(c['R'], c['B']),(0,0,1))

    cv2.imshow('02 - out', img_out)
    cv2.imwrite('02 - out.png', img_out*255)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

#===============================================================================
