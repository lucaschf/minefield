from minesweeper import Minesweeper
from data import config

def matriz(players):
    matrizConfig = config(players)

    line = matrizConfig['line']
    column = matrizConfig['column']
    bombs = matrizConfig['bombs']
    minesweeper = Minesweeper(line,column,bombs)

    matriz = minesweeper.createMatriz()
    matriz = minesweeper.plantBombs(matriz)
    minesweeper.printMatriz(matriz)

    return matriz

matriz(1)