from minesweeper import Minesweeper

def matriz(players):
    minesweeper = Minesweeper(players)

    matriz = minesweeper.createMatriz()
    matriz = minesweeper.plantBombs(matriz)
    minesweeper.printMatriz(matriz)

    matriz = minesweeper.fieldLogic(0,0,matriz)


    return matriz

matriz(1)
