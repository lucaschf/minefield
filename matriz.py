from minesweeper import Minesweeper
from data import config

def matriz(players):
    minesweeper = Minesweeper(players)

    matriz = minesweeper.createMatriz()
    matriz = minesweeper.plantBombs(matriz)
    minesweeper.printMatriz(matriz)

    return matriz

matriz(1)