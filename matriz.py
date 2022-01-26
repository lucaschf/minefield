from minesweeper import Minesweeper

def matriz(players):
    minesweeper = Minesweeper(players)

    matriz = minesweeper.createMatriz()
    matriz = minesweeper.plantBombs(matriz)
    minesweeper.printMatriz(matriz)

    fieldData = minesweeper.fieldLogic(0,2,matriz)
    print(fieldData)

matriz(1)
