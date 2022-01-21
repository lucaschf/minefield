from random import randint

def createMatriz(l, c):
    matriz = [] # lista vazia
    for i in range(l):
        # cria a linha i
        linha = [] # lista vazia
        for j in range(c):
            linha += [0]

        # coloque linha na matriz
        matriz += [linha]
        # print(linha)

    return matriz

def printMatriz(matriz, line, column):
    for i in range(line):
        for j in range(column):
            print(str(matriz[i][j])+'  ', end="")
        print('\n')

def fillSides(matriz, x, y, line, column):

    # Ir para direita
    if(y+1 < column and matriz[x][y+1] != 9):
        matriz[x][y+1] += 1

    # Ir para esquerda
    if(y-1 >= 0 and matriz[x][y-1] != 9):
        matriz[x][y-1] += 1
    

    # Para cima
    if(x-1 >= 0 and matriz[x-1][y] != 9):
        matriz[x-1][y] += 1

    # Para baixo
    if(x+1 < line and matriz[x+1][y] != 9):
        matriz[x+1][y] += 1

    #Para cima e direita
    if(x-1 >= 0 and y+1 < column and matriz[x-1][y+1] != 9):
        matriz[x-1][y+1] += 1
    
    # Para baixo e direita
    if(x+1 < line and y+1 < column and matriz[x+1][y+1] != 9):
        matriz[x+1][y+1] += 1

    # Para cima e esquerda
    if(x-1 >=0 and y-1 >= 0 and matriz[x-1][y-1] != 9):
        matriz[x-1][y-1] += 1

    # Para baixo e esquerda
    if(x+1 < line and y-1 >=0 and matriz[x+1][y-1] != 9):
        matriz[x+1][y-1] += 1


    return matriz

def plantBombs(matriz, line, column, quantity):
    while (quantity > 0):
        bomb = True
        while(bomb):
            # Realiza o sorteio de uma linha e coluna
            x = randint(0, line-1)
            y = randint(0, column-1)

            # Verifica se a posição na matriz possui bomba
            if(matriz[x][y] != 9):
                bomb = False
                matriz[x][y] = 9
                matriz = fillSides(matriz, x, y, line, column)

        quantity -= 1

    return matriz


def init():
    line = 16
    column = 20
    quantity = 40  # Quantidade de bombas

    # Cria a matriz inicializando com 0
    matriz = createMatriz(line, column)

    matriz = plantBombs(matriz, line, column, quantity)
    printMatriz(matriz, line, column)

init()
