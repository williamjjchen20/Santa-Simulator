from cmu_graphics import *
import random, math, copy
from PIL import Image
import os, pathlib

#Houses
class House:
    def __init__(self, number, row, col):
        self.number = number
        self.row = row
        self.col = col
        self.gift = None

    def __repr__(self):
        return f'house at ({self.row}, {self.col})'
    
    def chooseGift(self, giftList):
        giftNum = random.randint(0, len(giftList)-1)
        self.gift = giftList[giftNum]

#Obstacles
class Obstacle:
    def __init__(self, number, row, col, type):
        self.number = number
        self.row = row
        self.col = col
        self.type = type

    def __repr__(self):
        return f'{self.type} at ({self.row}, {self.col})'
    
class Gift:
    def __init__(self, number, x, y, type):
        self.number = number
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return self.type

class Material:
    def __init__(self, number, x, y, type):
        self.number = number
        self.x = x
        self.y = y
        self.type = type

    def __repr__(self):
        return self.type
###

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def resetApp(app):
    app.screen = 'default-screen'
    ### Board characteristics 
    app.rows = 15
    app.cols = 15
    app.boardLeft = 0
    app.boardTop = 0
    app.inventoryWidth = 200
    app.bottomHeight = 100
    app.boardWidth = app.width-app.inventoryWidth
    app.inventoryLeft = app.boardWidth
    app.boardHeight = app.height - app.bottomHeight
    app.cellWidth, app.cellHeight = getCellSize(app)

    ### More Board
    app.board = [[0]*app.cols for i in range(app.rows)]

    ### Santa
    app.santaRow = 0
    app.santaCol = 0

    ### Setup Board
    resetBoard(app)

    ### Gifts
    app.giftList = ['teddy'] #, 'TV', 'coal', 'soldier', 'candycane']
    app.inventoryList = ['teddy'] #, 'TV', 'coal', 'soldier', 'candycane']
    app.inventory = []
    app.numGifts = 2
    app.giftsDelivered = 0
    app.maxGifts = (app.boardHeight-75)//75
    generateGifts(app)
    setUpInventory(app)
    app.selectedGift = None

    ### Gifts Setup
    app.teddyImage = openImage('teddy.jpg')
    app.teddyImage = CMUImage(app.teddyImage)
    app.teddyImageWidth, app.teddyImageHeight = 2*app.cellWidth, 2*app.cellHeight

    app.giftDict = {'teddy':app.teddyImage, 'TV':'gray', 'coal':'black', 'soldier':'green', 'candycane':'red'}

    ### Tool shop
    app.materialsList = ['wool', 'candy', 'plastic', 'metal', 'material5', 'material6']
    app.materialsBar = []
    app.materialsDict = {}
    app.materials = []
    app.selectedMaterial = None
    app.maxMaterials = 10
    app.tools = ['hammer', 'glue', 'oven', 'knit', 'paper']
    app.toolsDict = {}
    setUpMaterials(app)


    ## Game Features
    app.points = 0
    app.trashX, app.trashY = app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2

    ### Images
    app.santaImage = openImage('santa2.jpg')
    app.santaImage = CMUImage(app.santaImage)
    app.santaImageWidth, app.santaImageHeight = app.cellWidth, app.cellHeight

    app.tree1Image = openImage('tree1.jpg')
    app.tree1Image = CMUImage(app.tree1Image)
    app.tree2Image = openImage('tree2.jpg')
    app.tree2Image = CMUImage(app.tree2Image)
    app.treeImageWidth, app.treeImageHeight = app.cellWidth, app.cellHeight
    
def resetBoard(app):
    app.board = [[0]*app.cols for i in range(app.rows)]

    ### Houses
    app.houses = []
    app.numHouses = 3
    generateHouses(app)

    ###Obstacles
    app.obstacles = []
    app.obstacleTypes = ['tree1', 'tree2']
    app.numObstacles = 80
    generateObstacles(app)
    if not isLegalBoard(app):
        resetBoard(app)

def onAppStart(app):
    resetApp(app)

def openImage(fileName):
        return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def isLegalBoard(app):
    for house in app.houses:
        moves = []
        #print(house.row, house.col, app.houses)
        possible = checkLegality(app, house.row, house.col, moves)
        # print(app.houses)
        # print(moves)
        if not possible:
            return False
    return True

def checkLegality(app, row, col, moves):
    if (row, col) == (app.santaRow, app.santaCol):
        moves.append((row, col))
        return True
    else:
        moves.append((row, col))
        for (drow, dcol) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if isLegalMove(app, row+drow, col+dcol) and (row+drow, col+dcol) not in moves:
                row += drow
                col += dcol
                solution = checkLegality(app, row, col, moves)
                if solution:
                    return True
                row -= drow
                col -= dcol
        return False
    
### Functionality 

def onMousePress(app, mouseX, mouseY):
    #Checks which gift is selected
    
    for gift in app.inventory:
        if distance(mouseX, mouseY, gift.x, gift.y)<25:
            app.selectedGift = gift.number

    if app.screen == 'gifts-screen':
        # if distance(mouseX, mouseY, app.width/2, app.height/2) < 50 and len(app.inventoryList) < app.maxGifts:
        #     randomGift = random.randint(0, len(app.giftList)-1)
        #     app.inventoryList.append(app.giftList[randomGift])
        #     setUpInventory(app)
        if len(app.materials) < app.maxMaterials:
            for materialIcon in app.materialsBar:
                if distance(mouseX, mouseY, materialIcon.x, materialIcon.y)<25:
                    newMaterial = Material(len(app.materials), mouseX, mouseY, materialIcon.type)
                    app.materials.append(newMaterial)
        for material in app.materials:
            if distance(mouseX, mouseY, material.x, material.y)<25:
                app.selectedMaterial = material.number

def onMouseDrag(app, mouseX, mouseY):
    if app.selectedGift != None:
        gift = app.inventory[app.selectedGift]
        gift.x, gift.y = mouseX, mouseY

    if app.selectedMaterial != None and app.screen == 'gifts-screen':
        material = app.materials[app.selectedMaterial]
        material.x, material.y = mouseX, mouseY
    
def onMouseRelease(app, mouseX, mouseY):
    if app.selectedGift != None:
        gift = app.inventory[app.selectedGift]
        if (app.boardWidth > mouseX and mouseX > 0) and (app.boardHeight > mouseY and mouseY > 0):
            dropRow, dropCol = getCell(app, mouseX, mouseY)
            #print(dropRow, dropCol)
            for house in app.houses:
                if house.row == dropRow and house.col == dropCol and house.gift == gift.type and isNearHouse(app, house):
                    app.points += 100 ###### add points when the gift goes to the right house
                    app.inventoryList.pop(gift.number)
                    app.inventory.pop(gift.number)
                    app.selectedGift = None
                    house.gift = None
                    app.giftsDelivered += 1
                    if app.giftsDelivered % 3 == 0:
                        resetBoard(app)               
                    resetInventory(app)
                    generateGifts(app)
        elif distance(mouseX, mouseY, app.trashX, app.trashY) < 30:
            app.inventory.pop(gift.number)
            app.inventoryList.pop(gift.number)
            app.selectedGift = None
            resetInventory(app)
        
        ### Resets gift position if not valid
        gift.x, gift.y = app.inventoryLeft + app.inventoryWidth/2, 75+75*gift.number
        app.selectedGift = None

    if app.selectedMaterial != None and app.screen == 'gifts-screen':
        material = app.materials[app.selectedMaterial]
        if (mouseX > 0 and mouseX < app.boardWidth) and (mouseY > 0 and mouseY < app.boardHeight):
            material.x, material.y = mouseX, mouseY
        else:
            app.materials.pop(material.number)
            resetMaterials(app)
        app.selectedMaterial = None

def onKeyPress(app, key):
    dcol, drow = None, None
    if key == 'right': #and app.santaRow < app.cols-2:
        app.santaCol += 1
        dcol, drow = 1, 0
    elif key == 'left': #and app.santaRow > 0:
        app.santaCol -=1
        dcol, drow = -1, 0
    elif key == 'down': #and app.santaCol < app.rows-2:
        app.santaRow += 1
        dcol, drow = 0, 1
    elif key == 'up': #and app.santaCol > 0:
        app.santaRow -= 1
        dcol, drow = 0, -1
    #print(app.santaRow, app.santaCol)
    moveCheck(app, dcol, drow)

    if key == 'r':
        resetApp(app)

    if key == 'g':
        if app.screen == 'default-screen':
            app.screen = 'gifts-screen'
        elif app.screen == 'gifts-screen':
            app.screen = 'default-screen'

def moveCheck(app, dcol, drow):
    if app.santaRow > app.rows-1 or app.santaRow < 0:
        app.santaRow -= drow
    elif app.santaCol > app.cols-1 or app.santaCol < 0:
        app.santaCol -= dcol
    elif app.board[app.santaRow][app.santaCol] == 'house' or app.board[app.santaRow][app.santaCol] in app.obstacleTypes:
        app.santaRow -= drow
        app.santaCol -= dcol

def isLegalMove(app, row, col):
    if row > app.rows-1 or row < 0:
        return False
    elif col > app.cols-1 or col < 0:
        return False
    elif app.board[row][col] == 'house' or app.board[row][col] in app.obstacleTypes:
        return False
    return True

def isNearHouse(app, house):
    for dcol, drow in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if house.col + dcol == app.santaCol and house.row + drow == app.santaRow:
            return True
    return False

### Graphics
def redrawAll(app):
    if app.screen == 'default-screen':
        redrawDefault(app)
    elif app.screen == 'gifts-screen':
        redrawGifts(app)

## Main Page
def redrawDefault(app):
    drawHouses(app)
    drawObstacles(app)
    drawSanta(app)
    drawInventory(app)
    drawBottomDefault(app)

def generateHouses(app):
    for i in range(app.numHouses):
        generateHouse(app, i)

def generateHouse(app, i):
    houseRow, houseCol = random.randint(1, app.rows-2), random.randint(1, app.cols-2)
    housePos = app.board[houseRow][houseCol]
    if housePos == 0 and not isClogged(app, houseRow, houseCol):
        app.board[houseRow][houseCol] = 'house'
    else:
        generateHouse(app, i)
        return
    app.houses.append(House(i, houseRow, houseCol))

def generateGifts(app):
    noneCount = countNone(app)
    while noneCount > app.numHouses - app.numGifts:
        randHouse = random.randint(0, app.numHouses-1)
        if app.houses[randHouse].gift == None:
            app.houses[randHouse].chooseGift(app.giftList)
            noneCount -= 1

def countNone(app):
    count = 0
    for house in app.houses:
        if house.gift == None:
            count += 1
    return count

def generateObstacles(app):
    for i in range(app.numObstacles):
        generateObstacle(app, i)
    
def generateObstacle(app, i):
    obsRow, obsCol = random.randint(0, app.rows-1), random.randint(0, app.cols-1)
    obsPos = app.board[obsRow][obsCol]
    randObs = random.randint(0, len(app.obstacleTypes)-1)
    if obsPos == 0 and (obsRow, obsCol) != (app.santaRow, app.santaCol): #and not isClogged(app, obsRow, obsCol):
        app.board[obsRow][obsCol] = app.obstacleTypes[randObs]
    else:
        generateObstacle(app, i)
        return
    app.obstacles.append(Obstacle(i, obsRow, obsCol, app.obstacleTypes[randObs]))
    
def isClogged(app, row, col):
    for house in app.houses:
        dist =((row-house.row)**2 + (col-house.col)**2)**0.5
        if dist <= 6:
            return True 
    return False

def drawHouses(app):
    for house in app.houses:
        houseX, houseY = house.col*app.cellWidth, house.row*app.cellHeight
        drawRect(houseX + app.cellWidth/6, houseY+app.cellHeight/2, 2*app.cellWidth/3, app.cellHeight/2, fill='sienna')
        drawPolygon(houseX, houseY+app.cellHeight/2, houseX+app.cellWidth/4, houseY+app.cellHeight/8, houseX+3*app.cellWidth/4, houseY+app.cellHeight/8, houseX+app.cellWidth, houseY+app.cellHeight/2, fill='red')
        #drawRect(houseX, houseY, app.cellWidth, app.cellHeight, fill='red')
        drawLabel(f'{house.gift}', houseX+app.cellWidth/2, houseY+app.cellHeight/2)

def drawObstacles(app):
    ### try to improve efficiency
    for obstacle in app.obstacles:
        obsX, obsY = obstacle.col*app.cellWidth, obstacle.row*app.cellHeight
        if obstacle.type == 'tree1':
            #drawImage(app.tree1Image, obsX, obsY, width=app.treeImageWidth, height=app.treeImageHeight)
            drawRect(obsX+4*app.cellWidth/10, obsY+4*app.cellHeight/5, app.cellWidth/5, app.cellHeight/5, fill='sienna')
            drawPolygon(obsX, obsY+4*app.cellHeight/5, obsX+app.cellWidth/2, obsY, obsX+app.cellWidth, obsY+4*app.cellHeight/5, fill='darkGreen', border='white', borderWidth=2.5)
            drawPolygon(obsX+app.cellWidth/8, obsY+app.cellHeight/2, obsX+app.cellWidth/2, obsY, obsX+7*app.cellWidth/8, obsY+app.cellHeight/2, fill='forestGreen', border='white', borderWidth=1.25)
            drawPolygon(obsX+app.cellWidth/6, obsY+app.cellHeight/4, obsX+app.cellWidth/2, obsY, obsX+5*app.cellWidth/6, obsY+app.cellHeight/4, fill='green', border='white', borderWidth=1.25)
        elif obstacle.type == 'tree2':
            #drawImage(app.tree2Image, obsX, obsY, width=app.treeImageWidth, height=app.treeImageHeight)
            drawRect(obsX+4*app.cellWidth/10, obsY+3*app.cellHeight/5, app.cellWidth/5, 2*app.cellHeight/5, fill='brown')
            drawPolygon(obsX+app.cellWidth/8, obsY+4*app.cellHeight/5, obsX+app.cellWidth/2, obsY, obsX+7*app.cellWidth/8, obsY+4*app.cellHeight/5, fill='darkOliveGreen', border='white')
            drawPolygon(obsX+app.cellWidth/6, obsY+app.cellHeight/2, obsX+app.cellWidth/2, obsY, obsX+5*app.cellWidth/6, obsY+app.cellHeight/2, fill='oliveDrab', border='white')
            drawPolygon(obsX+app.cellWidth/4, obsY+app.cellHeight/4, obsX+app.cellWidth/2, obsY, obsX+3*app.cellWidth/4, obsY+app.cellHeight/4, fill='olive', border='white')
        else:
            drawRect(obsX, obsY, app.cellWidth, app.cellHeight, fill='green')
        #drawLabel(f'{obstacle.number+1}', obsX+cellWidth/2, obsY+cellHeight/2)

def drawSanta(app):
    cx, cy = app.santaCol*app.cellWidth, app.santaRow*app.cellHeight
    drawImage(app.santaImage, cx, cy, width=app.santaImageWidth, height=app.santaImageHeight)
    #drawCircle(cx + cellWidth/2, cy + cellHeight/2, 10, fill='blue')

def setUpInventory(app):
    for i in range(len(app.inventoryList)):
        if i >= len(app.inventory): ## adds new gifts into inventory without duplicating old gifts
            giftName = app.inventoryList[i]
            x, y = app.inventoryLeft + app.inventoryWidth/2, 75+75*i
            gift = Gift(i, x, y, giftName)
            app.inventory.append(gift)

def resetInventory(app):
    for i in range(len(app.inventoryList)):
        gift = app.inventory[i]
        gift.number = i
        gift.x, gift.y = app.inventoryLeft + app.inventoryWidth/2, 75+75*i

def drawInventory(app):
    drawLine(app.boardWidth, 0, app.boardWidth, app.height)
    drawLabel('Gifts', app.boardWidth+app.inventoryWidth/2, 20, align='center', size=20)

    for i in range(len(app.inventoryList)):
        gift = app.inventory[i]
        x, y = gift.x, gift.y
        #drawCircle(x, y, 25, fill=app.giftDict[gift.type], align='center')
        drawImage(app.giftDict[gift.type], x, y, width=app.teddyImageWidth, height=app.teddyImageHeight, align='center')
        drawLabel(gift.type, x, y)
    
    drawCircle(app.trashX, app.trashY, 30, align='center', fill='gray')
    drawLabel('Trash Can', app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2)
    
def drawBottomDefault(app):
    drawLabel(f'Points: {app.points}', app.boardWidth/6, app.boardHeight + app.bottomHeight/2, size=20)
    drawLabel(f"Press 'g' to make gifts!", app.boardWidth/2, app.boardHeight + app.bottomHeight/2, size=16)
    drawLabel(f'Time', 5*app.boardWidth/6, app.boardHeight + app.bottomHeight/2, size=20)

    drawLine(0, app.boardHeight, app.boardWidth, app.boardHeight)

## Gift page
def setUpMaterials(app):
    for i in range(len(app.materialsList)):
        x, y = 35+(app.boardWidth/len(app.materialsList))*i, app.boardHeight+app.bottomHeight/2
        app.materialsBar.append(Material(i, x, y, app.materialsList[i]))

def resetMaterials(app):
    for i in range(len(app.materials)):
        material = app.materials[i]
        material.number = i

def redrawGifts(app):
    drawInventory(app)
    drawTools(app)
    drawMaterials(app)
    drawBottomGifts(app)

def drawTools(app):
    pass

def drawMaterials(app):
    for i in range(len(app.materialsBar)):
        material = app.materialsBar[i]
        cx, cy = material.x, material.y
        drawCircle(cx, cy, 25, fill='gray')
        drawLabel(f'{material.type}', cx, cy)
    for material in app.materials:
        drawCircle(material.x, material.y, 25, fill='gray')
        drawLabel(f'{material.type}', material.x, material.y)

def drawBottomGifts(app):
    drawTools(app)
    drawLine(0, app.boardHeight, app.boardWidth, app.boardHeight)

####### Creating the Board ####### credit: CSAcademy
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

def main():
    runApp(800, 700)

main()