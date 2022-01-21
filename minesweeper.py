from random import randint

class Minesweeper:
    def __init__(self, line, column, bombs):
        self.line = line
        self.column = column
        self.bombs = bombs

    def createMatriz(self):
        matriz = [] # lista vazia
        for i in range(self.line):
            # cria a linha i
            linha = [] # lista vazia
            for j in range(self.column):
                linha += [0]

            # coloque linha na matriz
            matriz += [linha]
            # print(linha)

        return matriz

    def printMatriz(self, matriz):
        for i in range(self.line):
            for j in range(self.column):
                print(str(matriz[i][j])+'  ', end="")
            print('\n')

    def fillSides(self, matriz, x, y):

        # Ir para direita
        if(y+1 < self.column and matriz[x][y+1] != 9):
            matriz[x][y+1] += 1

        # Ir para esquerda
        if(y-1 >= 0 and matriz[x][y-1] != 9):
            matriz[x][y-1] += 1
        

        # Para cima
        if(x-1 >= 0 and matriz[x-1][y] != 9):
            matriz[x-1][y] += 1

        # Para baixo
        if(x+1 < self.line and matriz[x+1][y] != 9):
            matriz[x+1][y] += 1

        #Para cima e direita
        if(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] != 9):
            matriz[x-1][y+1] += 1
        
        # Para baixo e direita
        if(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] != 9):
            matriz[x+1][y+1] += 1

        # Para cima e esquerda
        if(x-1 >=0 and y-1 >= 0 and matriz[x-1][y-1] != 9):
            matriz[x-1][y-1] += 1

        # Para baixo e esquerda
        if(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] != 9):
            matriz[x+1][y-1] += 1


        return matriz

    def plantBombs(self, matriz):
        while (self.bombs > 0):
            bomb = True
            while(bomb):
                # Realiza o sorteio de uma linha e coluna
                x = randint(0, self.line-1)
                y = randint(0, self.column-1)

                # Verifica se a posição na matriz possui bomba
                if(matriz[x][y] != 9):
                    bomb = False
                    matriz[x][y] = 9
                    matriz = self.fillSides(matriz, x, y)

            self.bombs -= 1

        return matriz