from queue import Queue
from random import randint

from dataclass.guess_result import GuessResult
from dataclass.minesweeper_DTO import MinesweeperDTO
from helpers.data import config


class Minesweeper:

    def __init__(self, players):
        self.__players = players
        self.__config = config(self.__players)
        self.line = self.__config["line"]
        self.column = self.__config["column"]
        self.bombs = self.__config["bombs"]
        self.positions = self.__config["availableFields"]
        self.totalCoordinates = []
        self.matriz = self.__createMatriz()
        self.__plantBombs()

    def __createMatriz(self):
        matriz = []  # lista vazia
        for i in range(self.line):
            # cria a linha i
            linha = []  # lista vazia
            for j in range(self.column):
                linha += [0]

            # coloque linha na matriz
            matriz += [linha]
            # print(linha)

        return matriz

    def __printMatriz(self, matriz):
        for i in range(self.line):
            for j in range(self.column):
                print(str(matriz[i][j]) + '  ', end="")
            print('\n')

    def __fillSides(self, matriz, x, y):

        # Ir para direita
        if (y + 1 < self.column and matriz[x][y + 1] != 9):
            matriz[x][y + 1] += 1

        # Ir para esquerda
        if (y - 1 >= 0 and matriz[x][y - 1] != 9):
            matriz[x][y - 1] += 1

        # Para cima
        if (x - 1 >= 0 and matriz[x - 1][y] != 9):
            matriz[x - 1][y] += 1

        # Para baixo
        if (x + 1 < self.line and matriz[x + 1][y] != 9):
            matriz[x + 1][y] += 1

        # Para cima e direita
        if (x - 1 >= 0 and y + 1 < self.column and matriz[x - 1][y + 1] != 9):
            matriz[x - 1][y + 1] += 1

        # Para baixo e direita
        if (x + 1 < self.line and y + 1 < self.column and matriz[x + 1][y + 1] != 9):
            matriz[x + 1][y + 1] += 1

        # Para cima e esquerda
        if (x - 1 >= 0 and y - 1 >= 0 and matriz[x - 1][y - 1] != 9):
            matriz[x - 1][y - 1] += 1

        # Para baixo e esquerda
        if (x + 1 < self.line and y - 1 >= 0 and matriz[x + 1][y - 1] != 9):
            matriz[x + 1][y - 1] += 1

        return matriz

    def __plantBombs(self):
        while self.bombs > 0:
            bomb = True

            while bomb:
                # Realiza o sorteio de uma linha e coluna
                x = randint(0, self.line - 1)
                y = randint(0, self.column - 1)

                # Verifica se a posição na matriz possui bomba
                if self.matriz[x][y] != 9:
                    bomb = False
                    self.matriz[x][y] = 9
                    self.matriz = self.__fillSides(self.matriz, x, y)

            self.bombs -= 1

        return self.matriz

    def __gameFinished(self):
        return len(self.totalCoordinates) == self.positions

    def __fieldZero(self, x, y, matriz, queue, coordinates):
        if (([x, y] in list(self.totalCoordinates)) == False):
            self.totalCoordinates.append([x, y])

        # Para cima
        if (x - 1 >= 0 and matriz[x - 1][y] == 0 and ([x - 1, y] in coordinates) == False and (
                [x - 1, y] in list(queue.queue)) == False):
            coordinates.append([x - 1, y])
            queue.put([x - 1, y])
            self.__fieldZero(x - 1, y, matriz, queue, coordinates)
        elif (x - 1 >= 0 and matriz[x - 1][y] != 0 and ([x - 1, y] in coordinates) == False):
            coordinates.append([x - 1, y])
            if (([x - 1, y] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x - 1, y])

        # Para cima e direita
        if (x - 1 >= 0 and y + 1 < self.column and matriz[x - 1][y + 1] == 0 and (
                [x - 1, y + 1] in coordinates) == False and ([x - 1, y + 1] in list(queue.queue)) == False):
            coordinates.append([x - 1, y + 1])
            queue.put([x - 1, y + 1])
            self.__fieldZero(x - 1, y + 1, matriz, queue, coordinates)
        elif (x - 1 >= 0 and y + 1 < self.column and matriz[x - 1][y + 1] != 0 and (
                [x - 1, y + 1] in coordinates) == False):
            coordinates.append([x - 1, y + 1])
            if (([x - 1, y + 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x - 1, y + 1])

        # Ir para direita
        if (y + 1 < self.column and matriz[x][y + 1] == 0 and ([x, y + 1] in coordinates) == False and (
                [x, y + 1] in list(queue.queue)) == False):
            coordinates.append([x, y + 1])
            queue.put([x, y + 1])
            self.__fieldZero(x, y + 1, matriz, queue, coordinates)
        elif (y + 1 < self.column and matriz[x][y + 1] != 0 and ([x, y + 1] in coordinates) == False):
            coordinates.append([x, y + 1])
            if (([x, y + 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x, y + 1])

        # Para baixo e direita
        if (x + 1 < self.line and y + 1 < self.column and matriz[x + 1][y + 1] == 0 and (
                [x + 1, y + 1] in coordinates) == False and ([x + 1, y + 1] in list(queue.queue)) == False):
            coordinates.append([x + 1, y + 1])
            queue.put([x + 1, y + 1])
            self.__fieldZero(x + 1, y + 1, matriz, queue, coordinates)
        elif (x + 1 < self.line and y + 1 < self.column and matriz[x + 1][y + 1] != 0 and (
                [x + 1, y + 1] in coordinates) == False):
            coordinates.append([x + 1, y + 1])
            if (([x + 1, y + 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x + 1, y + 1])

        # Para baixo
        if (x + 1 < self.line and matriz[x + 1][y] == 0 and ([x + 1, y] in coordinates) == False and (
                [x + 1, y] in list(queue.queue)) == False):
            coordinates.append([x + 1, y])
            queue.put([x + 1, y])
            self.__fieldZero(x + 1, y, matriz, queue, coordinates)
        elif (x + 1 < self.line and matriz[x + 1][y] != 0 and ([x + 1, y] in coordinates) == False):
            coordinates.append([x + 1, y])
            if (([x + 1, y] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x + 1, y])

        # Para baixo e esquerda
        if (x + 1 < self.line and y - 1 >= 0 and matriz[x + 1][y - 1] == 0 and (
                [x + 1, y - 1] in coordinates) == False and ([x + 1, y - 1] in list(queue.queue)) == False):
            coordinates.append([x + 1, y - 1])
            queue.put([x + 1, y - 1])
            self.__fieldZero(x + 1, y - 1, matriz, queue, coordinates)
        elif (x + 1 < self.line and y - 1 >= 0 and matriz[x + 1][y - 1] != 0 and (
                [x + 1, y - 1] in coordinates) == False):
            coordinates.append([x + 1, y - 1])
            if (([x + 1, y - 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x + 1, y - 1])

        # Ir para esquerda
        if (y - 1 >= 0 and matriz[x][y - 1] == 0 and ([x, y - 1] in coordinates) == False and (
                [x, y - 1] in list(queue.queue)) == False):
            coordinates.append([x, y - 1])
            queue.put([x, y - 1])
            self.__fieldZero(x, y - 1, matriz, queue, coordinates)
        elif (y - 1 >= 0 and matriz[x][y - 1] != 0 and ([x, y - 1] in coordinates) == False):
            coordinates.append([x, y - 1])
            if (([x, y - 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x, y - 1])

        # Para cima e esquerda
        if (x - 1 >= 0 and y - 1 >= 0 and matriz[x - 1][y - 1] == 0 and ([x - 1, y - 1] in coordinates) == False and (
                [x - 1, y - 1] in list(queue.queue)) == False):
            coordinates.append([x - 1, y - 1])
            queue.put([x - 1, y - 1])
            self.__fieldZero(x - 1, y - 1, matriz, queue, coordinates)
        elif (x - 1 >= 0 and y - 1 >= 0 and matriz[x - 1][y - 1] != 0 and ([x - 1, y - 1] in coordinates) == False):
            coordinates.append([x - 1, y - 1])
            if (([x - 1, y - 1] in list(self.totalCoordinates)) == False):
                self.totalCoordinates.append([x - 1, y - 1])

    def verify_position(self, x, y):
        print('\n')

        if self.matriz[x][y] == 0:
            queue = Queue()
            queue.put([x, y])
            coordinates = [[x, y]]

            self.__fieldZero(x, y, self.matriz, queue, coordinates)

            score = len(coordinates)*10
            won = self.__gameFinished()
            return GuessResult(False, coordinates, won, score)

        elif self.matriz[x][y] == 9:
            return GuessResult(True, [x, y], False, 0)
        else:
            if not ([x, y] in list(self.totalCoordinates)):
                self.totalCoordinates.append([x, y])

            won = self.__gameFinished()
            return GuessResult(False, [x, y], won, 10)

    def to_dto(self):
        return MinesweeperDTO(self.__config, tuple(self.totalCoordinates), tuple(self.matriz))
