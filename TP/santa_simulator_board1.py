from cmu_graphics import *
import random, math
from PIL import Image
import os, pathlib

####### Creating the Board ####### credit: CSAcademy, link: https://academy.cs.cmu.edu/notes/5504
def getCellSize(app):
    cellWidth = app.boardWidth/app.cols
    cellHeight = app.boardHeight/app.rows
    return (cellWidth, cellHeight)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    col = math.floor(dx/cellHeight) 
    row = math.floor(dy/cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
######## Board Creation #######