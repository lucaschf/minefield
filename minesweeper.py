from random import randint
from data import config
from field import Field

class Minesweeper:
    def __init__(self, players):
        self.__players = players
        self.__config = config(self.__players)
        self.line = self.__config["line"]
        self.column = self.__config["column"]
        self.bombs = self.__config["bombs"]

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

    def fieldLogic(self,x,y,matriz):
        print('\n')

        if(matriz[x][y] == 0):
            print('abrir campos adjacentes')
        elif matriz[x][y] == 9:
            fieldData = Field(True, [x, y], False)
            print('bomba',fieldData)
            return fieldData
        else:
            fieldData = Field(False, [x, y], False)
            print('campo comum',fieldData)
            return fieldData

        self.printMatriz(matriz)

        return matriz
