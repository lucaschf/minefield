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
            matriz[x][y] = 'x'
            self.validateLine(matriz,x,y)

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

    def validateLine(self, matriz,x,y):
        # Direita
        if(y+1 < self.column  and matriz[x][y+1] == 0):
            matriz[x][y+1] = 'x'
            self.right(matriz,x,y+1)
        elif(y+1 < self.column  and matriz[x][y+1] != 0):
            matriz[x][y+1] = 'x'

        # Esquerda
        if(y-1 >= 0 and matriz[x][y-1] == 0):
            matriz[x][y-1] = 'x'
            self.left(matriz,x,y-1)
        elif(y-1 >= 0 and matriz[x][y-1] != 0):
            matriz[x][y-1] = 'x'

        # Baixo
        if(x+1 < self.line and matriz[x+1][y] == 0):
            matriz[x+1][y] = 'x'
            self.down(matriz,x+1,y)
        elif(x+1 < self.line and matriz[x+1][y] != 0):
            matriz[x+1][y] = 'x'

        # Cima
        if(x-1 >= 0 and matriz[x-1][y] == 0):
            matriz[x-1][y] = 'x'
            self.up(matriz,x-1,y)
        elif(x-1 >= 0 and matriz[x-1][y] != 0):
            matriz[x-1][y] = 'x'

        # Cima/Direita
        if(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] == 0):
            matriz[x-1][y+1] = 'x'
            self.upRight(matriz,x-1,y)
        elif(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] != 0):
            matriz[x-1][y+1] = 'x'

        # Baixo/Direita
        if(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] == 0):
            matriz[x+1][y+1] = 'x'
            self.downRight(matriz,x-1,y)
        elif(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] != 0):
            matriz[x+1][y+1] = 'x'

        # Cima/esquerda
        if(x-1 >=0 and y-1 >= 0 and  matriz[x-1][y-1] == 0):
            matriz[x-1][y-1] = 'x'
            self.upLeft(matriz,x-1,y)
        elif(x-1 >=0 and y-1 >= 0 and  matriz[x-1][y-1] != 0):
            matriz[x-1][y-1] = 'x'

        # Baixo/esquerda
        if(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] == 0):
            matriz[x+1][y-1] = 'x'
            self.downLeft(matriz,x-1,y)
        elif(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] != 0):
            matriz[x+1][y-1] = 'x'


    # AÇÕES
    def right(self, matriz,x,y):
        if(y+1 < self.column  and matriz[x][y+1] == 0):
            matriz[x][y+1] = 'x'
            self.validateLine(matriz,x,y+1)
        elif(y+1 < self.column  and matriz[x][y+1] != 0):
            matriz[x][y+1] = 'x'

    def left(self, matriz,x,y):
        if(y-1 >= 0 and matriz[x][y-1] == 0):
            matriz[x][y-1] = 'x'
            self.validateLine(matriz,x,y-1)
        elif(y-1 >= 0 and matriz[x][y-1] != 0):
            matriz[x][y-1] = 'x'

    def down(self, matriz,x,y):
        if(x+1 < self.line and matriz[x+1][y] == 0):
            matriz[x+1][y] = 'x'
            self.validateLine(matriz,x+1,y)
        elif(x+1 < self.line and matriz[x+1][y] != 0):
            matriz[x+1][y] = 'x'

    def up(self, matriz,x,y):
        if(x-1 >= 0 and matriz[x-1][y] == 0):
            matriz[x-1][y] = 'x'
            self.validateLine(matriz,x-1,y)
        elif(x-1 >= 0 and matriz[x-1][y] != 0):
            matriz[x-1][y] = 'x'

    def upRight(self, matriz,x,y):
        if(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] == 0):
            matriz[x-1][y+1] = 'x'
            self.validateLine(matriz,x-1,y)
        elif(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] != 0):
            matriz[x-1][y+1] = 'x'

    def downRight(self, matriz,x,y):
        if(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] == 0):
            matriz[x+1][y+1] = 'x'
            self.validateLine(matriz,x-1,y)
        elif(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] != 0):
            matriz[x+1][y+1] = 'x'

    def upLeft(self, matriz,x,y):
        if(x-1 >=0 and y-1 >= 0 and  matriz[x-1][y-1] == 0):
            matriz[x-1][y-1] = 'x'
            self.validateLine(matriz,x-1,y)
        elif(x-1 >=0 and y-1 >= 0 and  matriz[x-1][y-1] != 0):
            matriz[x-1][y-1] = 'x'

    def downLeft(self, matriz,x,y):
        if(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] == 0):
            matriz[x+1][y-1] = 'x'
            self.validateLine(matriz,x-1,y)
        elif(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] != 0):
            matriz[x+1][y-1] = 'x'


    def fieldZero(self,x,y,matriz):
        # Ir para direita
        if(y+1 < self.column and matriz[x][y+1] != 9):
            if(matriz[x][y+1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x][y+1] = 'x'

        # Ir para esquerda
        if(y-1 >= 0 and matriz[x][y-1] != 9):
            if(matriz[x][y-1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x][y-1] = 'x'
        

        # Para cima
        if(x-1 >= 0 and matriz[x-1][y] != 9):
            if(matriz[x-1][y]  == 0):
                self.fieldZero(x,y,matriz)
            matriz[x-1][y] = 'x'

        # Para baixo
        if(x+1 < self.line and matriz[x+1][y] != 9):
            if(matriz[x+1][y] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x+1][y] = 'x'

        #Para cima e direita
        if(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] != 9):
            if(matriz[x-1][y+1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x-1][y+1] = 'x'
        
        # Para baixo e direita
        if(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] != 9):
            if(matriz[x+1][y+1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x+1][y+1] = 'x'

        # Para cima e esquerda
        if(x-1 >=0 and y-1 >= 0 and matriz[x-1][y-1] != 9):
            if(matriz[x-1][y-1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x-1][y-1] = 'x'

        # Para baixo e esquerda
        if(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] != 9):
            if(matriz[x+1][y-1] == 0):
                self.fieldZero(x,y,matriz)
            matriz[x+1][y-1] = 'x'
        
