from random import randint
from data import config
from field import Field
from queue import Queue

class Minesweeper:
    def __init__(self, players):
        self.__players = players
        self.__config = config(self.__players)
        self.line = self.__config["line"]
        self.column = self.__config["column"]
        self.bombs = self.__config["bombs"]
        self.positions = self.__config["availableFields"] 
        self.totalCoordinates = []


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

    def gameFinished(self):
        if(len(self.totalCoordinates) == self.positions):
            return True
        else:
            return False

    def fieldLogic(self,x,y,matriz):
        print('\n')

        if(matriz[x][y] == 0):
            queue = Queue()
            queue.put([x,y])
            coordinates = []
            coordinates.append([x,y])

            self.fieldZero(x,y,matriz,queue,coordinates)

            print('abrir campos adjacentes', coordinates)
            won = self.gameFinished()
            return Field(True, coordinates, won)

        elif matriz[x][y] == 9:
            print('bomba')

            if(([x,y] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x,y])

            won = self.gameFinished()
            return Field(True, [x, y], won)
        else:
            print('campo comum')

            if(([x,y] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x,y])

            won = self.gameFinished()
            return Field(False, [x, y], won)


    def fieldZero(self,x,y,matriz,queue,coordinates):
        if(([x,y] in list(self.totalCoordinates)) == False):
            self.totalCoordinates.append([x,y])

        # Para cima
        if(x-1 >= 0 and matriz[x-1][y] == 0 and ([x-1,y] in coordinates) == False and ([x-1,y] in list(queue.queue)) == False):
                coordinates.append([x-1,y])
                queue.put([x-1,y])
                self.fieldZero(x-1,y,matriz,queue,coordinates)
        elif(x-1 >= 0 and matriz[x-1][y] != 0 and ([x-1,y] in coordinates) == False):
            coordinates.append([x-1,y])
            if(([x-1,y]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x-1,y])

        #Para cima e direita
        if(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] == 0 and ([x-1,y+1] in coordinates) == False and ([x-1,y+1] in list(queue.queue)) == False):
                coordinates.append([x-1,y+1])
                queue.put([x-1,y+1])
                self.fieldZero(x-1,y+1,matriz,queue,coordinates)
        elif(x-1 >= 0 and y+1 < self.column and matriz[x-1][y+1] != 0 and ([x-1,y+1] in coordinates) == False):
            coordinates.append([x-1,y+1])
            if(([x-1,y+1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x-1,y+1])

        # Ir para direita
        if(y+1 < self.column and matriz[x][y+1] == 0 and ([x,y+1] in coordinates) == False and ([x,y+1] in list(queue.queue)) == False):
                coordinates.append([x,y+1])
                queue.put([x,y+1])
                self.fieldZero(x,y+1,matriz,queue,coordinates)
        elif(y+1 < self.column and matriz[x][y+1] != 0 and ([x,y+1] in coordinates) == False):
            coordinates.append([x,y+1])
            if(([x,y+1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x,y+1])

        # Para baixo e direita
        if(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] == 0 and ([x+1,y+1] in coordinates) == False and ([x+1,y+1] in list(queue.queue)) == False):
                coordinates.append([x+1,y+1])
                queue.put([x+1,y+1])
                self.fieldZero(x+1,y+1,matriz,queue,coordinates)
        elif(x+1 < self.line and y+1 < self.column and matriz[x+1][y+1] != 0 and ([x+1,y+1] in coordinates) == False):
            coordinates.append([x+1,y+1])
            if(([x+1,y+1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x+1,y+1])

        # Para baixo
        if(x+1 < self.line and matriz[x+1][y] == 0 and ([x+1,y] in coordinates) == False and ([x+1,y] in list(queue.queue)) == False):
                coordinates.append([x+1,y])
                queue.put([x+1,y])
                self.fieldZero(x+1,y,matriz,queue,coordinates)
        elif(x+1 < self.line and matriz[x+1][y] != 0 and ([x+1,y] in coordinates) == False):
            coordinates.append([x+1,y])
            if(([x+1,y]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x+1,y])

        # Para baixo e esquerda
        if(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] == 0 and ([x+1,y-1] in coordinates) == False and ([x+1,y-1] in list(queue.queue)) == False):
                coordinates.append([x+1,y-1])
                queue.put([x+1,y-1])
                self.fieldZero(x+1,y-1,matriz,queue,coordinates)
        elif(x+1 < self.line and y-1 >=0 and matriz[x+1][y-1] != 0 and ([x+1,y-1] in coordinates) == False):
            coordinates.append([x+1,y-1])
            if(([x+1,y-1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x+1,y-1])

        # Ir para esquerda
        if(y-1 >= 0 and matriz[x][y-1] == 0  and ([x,y-1] in coordinates) == False and ([x,y-1] in list(queue.queue)) == False):
                coordinates.append([x,y-1])
                queue.put([x,y-1])
                self.fieldZero(x,y-1,matriz,queue,coordinates)
        elif(y-1 >= 0 and matriz[x][y-1] != 0  and ([x,y-1] in coordinates) == False):
            coordinates.append([x,y-1])
            if(([x,y-1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x,y-1])

        # Para cima e esquerda
        if(x-1 >=0 and y-1 >= 0 and matriz[x-1][y-1] == 0 and ([x-1,y-1] in coordinates) == False and ([x-1,y-1] in list(queue.queue)) == False):
                coordinates.append([x-1,y-1])
                queue.put([x-1,y-1])
                self.fieldZero(x-1,y-1,matriz,queue,coordinates)
        elif(x-1 >=0 and y-1 >= 0 and matriz[x-1][y-1] != 0 and ([x-1,y-1] in coordinates) == False):
            coordinates.append([x-1,y-1])
            if(([x-1,y-1]in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x-1,y-1])

        
