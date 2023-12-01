from santa_simulator_board1 import *
from santa_simulator_images import * 
from santa_simulator_classes import *

from cmu_graphics import *
import random

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def resetApp(app, level, totalGifts, resetGame):

    app.screen = 'default-screen'
    app.level = level
    app.totalGifts = totalGifts
    app.totalLevels = 5
    
    app.paused = resetGame
    app.gameStart = resetGame
    app.gameOver = True if app.level > app.totalLevels else False

    ## Board characteristics 
    chooseBoardDimensions(app, app.level)
    app.boardLeft = 0
    app.boardTop = 0
    app.inventoryWidth = 200
    app.bottomHeight = 100
    app.boardWidth = app.width-app.inventoryWidth
    app.inventoryLeft = app.boardWidth
    app.boardHeight = app.height - app.bottomHeight
    app.cellWidth, app.cellHeight = getCellSize(app)

    #print(app.rows, app.cols)

    ### Santa
    app.santaRow = 0
    app.santaCol = 0

    ### Setup Board
    numObstacles = 40+10*app.level
    resetBoard(app, app.level, numObstacles)

    if resetGame:
        ### Gifts
        app.giftList = ['teddy', 'TV', 'shoes', 'soldier', 'candycane', 'sewing']
        app.giftImageDict = {'teddy':app.teddyImage, 'TV':app.TVImage, 'shoes':app.shoesImage, 'soldier':app.soldierImage, 'candycane':app.candycaneImage, 'sewing':app.sewingImage}
        app.inventoryList = []
        app.inventory = []
        app.numGifts = 1
        app.giftsDelivered = 0
        app.maxGifts = (app.boardHeight-75)//75
        generateGifts(app, 0)
        setUpInventory(app)
        app.selectedGift = None

        ### Tool shop
        app.materialsList = ['wool', 'candy', 'plastic', 'metal', 'wood']
        app.materialImageDict = {'wool': app.woolImage, 'candy': app.candyImage, 'plastic': app.plasticImage, 'metal': app.metalImage, 'wood': app.woodImage}
        app.materialsBar = []
        app.materialsDict = dict()
        app.materials = []
        app.selectedMaterial = None
        app.maxMaterials = 3
        app.tools = dict()
        app.toolImageDict = {'hammer': app.hammerImage, 'glue': app.glueImage, 'oven': app.ovenImage, 'knit': app.knitImage}
        app.selectedTool = None
        app.showRecipeBook = False
        app.recipeWidth, app.recipeHeight = 3*app.width/4, 3*app.height/4

        app.recipes = {
            'soldier': {'plastic': 2, 'tool': 'glue'},
            'teddy': {'wool': 2, 'tool': 'knit'},
            'TV': {'metal': 2, 'plastic': 1, 'tool': 'hammer'},
            'shoes': {'wood': 2, 'plastic': 1, 'tool': 'glue'},
            'candycane': {'candy': 2, 'tool': 'oven'},
            'sewing': {'metal': 1, 'wool': 1, 'wood': 1, 'tool': 'hammer'}
        }

        setUpMaterials(app)
        setUpTools(app)

        ## Game Features
        app.points = 0
        app.trashX, app.trashY = app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2
        app.gameTimer = 300
        app.timer = 0
        app.stepsPerSecond = 1

    ### Images
    app.santaImageWidth, app.santaImageHeight = app.cellWidth, app.cellHeight
    app.houseImageWidth, app.houseImageHeight = 1.3*app.cellWidth, 1.2*app.cellHeight
    app.materialImageWidth, app.materialImageHeight = 50, 50
    app.giftImageWidth, app.giftImageHeight = 60, 60

    print(app.rows, app.cols, app.numObstacles)

def chooseBoardDimensions(app, level):
    app.rows = 11 + level
    app.cols = 11 + level
    
def resetBoard(app, numHouses, numObstacles):
    app.board = [[0]*app.cols for i in range(app.rows)]
    ### Houses
    app.houses = []
    app.numHouses = numHouses
    generateHouses(app)

    ###Obstacles
    app.obstacles = []
    app.obstacleTypes = ['tree1', 'tree2']
    app.numObstacles = numObstacles
    generateObstacles(app)

    if not isLegalBoard(app):
        app.resetCounter += 1
        print(app.resetCounter)
        if app.resetCounter > 5:
            app.resetCounter = 0
            resetBoard(app, numHouses, numObstacles - 5) 
        else:
            resetBoard(app, app.numHouses, numObstacles)
        

def onAppStart(app):
    app.resetCounter = 0
    resetApp(app, 5, 0, True)

### Maze generation
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

def onStep(app):
    app.timer += 1
    if not app.gameOver:
        if not app.paused:
            app.gameTimer -= 1
        if app.gameTimer == 0:
            app.gameOver = True

def onMousePress(app, mouseX, mouseY):
    #Checks which gift is selected
    if not app.paused:
        for gift in app.inventory:
            if distance(mouseX, mouseY, gift.x, gift.y)<25:
                app.selectedGift = gift.number

        if app.screen == 'gifts-screen':
            if len(app.materials) < app.maxMaterials:
                for materialIcon in app.materialsBar:
                    if distance(mouseX, mouseY, materialIcon.x, materialIcon.y)<25:
                        newMaterial = Material(len(app.materials), mouseX, mouseY, materialIcon.type)
                        app.materials.append(newMaterial)

            for material in app.materials:
                if distance(mouseX, mouseY, material.x, material.y)<25 and app.selectedTool == None:
                    app.selectedMaterial = material.number
            
            for tool in app.tools:
                x, y = app.tools[tool].x, app.tools[tool].y
                if distance(mouseX, mouseY, x, y) < app.tools[tool].hitR and app.selectedMaterial == None and tool != 'oven':
                    app.selectedTool = tool
            
            if distance(mouseX, mouseY, app.trashX, app.trashY) < 30:
                app.materials = []
                resetTools(app)
            
def onMouseDrag(app, mouseX, mouseY):
    if not app.paused:
        if app.selectedGift != None:
            gift = app.inventory[app.selectedGift]
            gift.x, gift.y = mouseX, mouseY

        if app.selectedMaterial != None and app.screen == 'gifts-screen':
            material = app.materials[app.selectedMaterial]
            material.x, material.y = mouseX, mouseY

        if app.selectedTool != None and app.screen == 'gifts-screen':
            tool = app.tools[app.selectedTool]
            tool.x, tool.y = mouseX, mouseY
    
def onMouseRelease(app, mouseX, mouseY):
    if not app.paused:
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
                        app.totalGifts += 1
                        if app.giftsDelivered == app.numHouses:
                            resetApp(app, app.level+1, app.totalGifts, False)
                            app.giftsDelivered = 0 
                            generateGifts(app, 0)
                        else:
                            generateGifts(app, house.number+1)              
                        resetInventory(app)
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
            if (mouseX > 0 and mouseX < app.boardWidth-material.hitR) and (mouseY > 0 and mouseY < app.boardHeight-material.hitR):
                material.x, material.y = mouseX, mouseY
                app.materialsDict[material.number] = (material.x, material.y)
                ### special case for the oven
                oven = app.tools['oven']
                if distance(mouseX, mouseY, oven.x, oven.y) < oven.hitR:
                    checkMaterials(app, oven)
            else:
                app.materials.pop(material.number)
                # if material.number in app.materialsDict:
                #     del app.materialsDict[material.number] ### del function
                resetMaterials(app)
            app.selectedMaterial = None
            #checkMaterials(app)

        if app.selectedTool != None and app.screen == 'gifts-screen':
            tool = app.tools[app.selectedTool]
            if (mouseX > 0 and mouseX < app.boardWidth-tool.hitR) and (mouseY > 0 and mouseY < app.boardHeight-tool.hitR):
                tool.x, tool.y = mouseX, mouseY
                checkMaterials(app, tool)
            else:
                tool.x, tool.y = tool.startX, tool.startY
            app.selectedTool = None

def onKeyPress(app, key):
    if key == 'space':
        if app.gameOver:
            resetApp(app, 1, 0, True)
            return
        elif app.gameStart:
            app.gameStart = False
        app.paused = not app.paused

    if  key =='r' and not app.gameStart: ### Restart game 
        resetApp(app, 1, 0, True)

    if not app.gameOver:   
        if not app.paused:
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

            if key == 'g':
                if app.screen == 'default-screen':
                    app.screen = 'gifts-screen'
                elif app.screen == 'gifts-screen':
                    app.screen = 'default-screen'

            if key == 'h' and app.screen == 'gifts-screen':
                app.showRecipeBook = not app.showRecipeBook
    
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
    if app.gameStart:
        drawStartScreen(app)
    else:
        if app.screen == 'default-screen':
            redrawDefault(app)
        elif app.screen == 'gifts-screen':
            redrawGifts(app)
        if app.paused:
            drawPaused(app)

    if app.gameOver:
        if app.level > app.totalLevels:
            drawGameComplete(app)    
        else:
            drawGameOver(app)


def drawPaused(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=90)
    drawLabel('Game Paused', app.width/2, app.height/2, fill='white', size=50, bold=True, align='center')
    drawLabel("Press 'space' to resume", app.width/2, app.height/2+50, fill='white', size=20, align='center')
    drawLabel("Press 'r' to restart", app.width/2, app.height/2+75, fill='white', size=20, align='center')

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    titleColor = 'red' if app.timer % 2 == 0 else 'green'
    labelColor = 'green' if app.timer % 2 == 0 else 'red'
    drawLabel('Santa Simulator', app.width/2, app.height/2, fill=titleColor, size=50, bold=True, align='center')
    drawLabel('Press space to start game!', app.width/2, app.height/2+50, fill=labelColor, italic=True, size=25, align='center')

def drawGameOver(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=90)
    color1 = 'red' if app.timer % 2 == 0 else 'green'
    color2 = 'green' if app.timer % 2 == 0 else 'red'
    drawLabel('Times Up!', app.width/2, app.height/2, size=50, fill=color1, bold=True, align='center')
    drawLabel(f'Gifts Delivered: {app.totalGifts}', app.width/2, app.height/2 + 50, fill=color2, size=20, align='center')
    drawLabel(f'Points: {app.points}', app.width/2, app.height/2 + 75, fill=color1, size=20, align='center')

    drawLabel("Press 'space' to restart", app.width/2, app.height/2 + 150, fill='white', size=20, align='center')

def drawGameComplete(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    color1 = 'red' if app.timer % 2 == 0 else 'green'
    color2 = 'green' if app.timer % 2 == 0 else 'red'
    drawLabel('Great Work, Santa!', app.width/2, app.height/2, size=50, fill=color1, bold=True, align='center')
    drawLabel(f'Gifts Delivered: {app.totalGifts}', app.width/2, app.height/2 + 50, fill=color2, size=20, align='center')
    drawLabel(f'Time Elapsed: {300-app.gameTimer} seconds', app.width/2, app.height/2 + 75, fill=color1, size=20, align='center')

    drawLabel("Press 'space' to play again", app.width/2, app.height/2 + 150, fill='black', size=20, align='center')

## Main Page
def redrawDefault(app):
    drawHouses(app)
    drawObstacles(app)
    drawSanta(app)
    drawInventory(app)
    drawGiftRequests(app)
    drawExtraDefault(app)

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

def generateGifts(app, houseNum):
    app.houses[houseNum].chooseGift(app.giftList)

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
        if dist <= 5:
            return True 
    return False

def drawHouses(app):
    housePics = [app.houseImage1, app.houseImage2, app.houseImage3]
    for house in app.houses:
        houseX, houseY = house.col*app.cellWidth, house.row*app.cellHeight
        drawImage(housePics[house.number%len(housePics)], houseX+app.cellWidth/2, houseY+app.cellHeight/2 + 2, width=app.houseImageWidth, height=app.houseImageHeight, align='center')

def drawObstacles(app):
    for obstacle in app.obstacles:
        obsX, obsY = obstacle.col*app.cellWidth, obstacle.row*app.cellHeight
        if obstacle.type == 'tree1':
            drawRect(obsX+4*app.cellWidth/10, obsY+4*app.cellHeight/5, app.cellWidth/5, app.cellHeight/5, fill='sienna')
            drawPolygon(obsX, obsY+4*app.cellHeight/5, obsX+app.cellWidth/2, obsY, obsX+app.cellWidth, obsY+4*app.cellHeight/5, fill='darkGreen', border='white', borderWidth=2.5)
            drawPolygon(obsX+app.cellWidth/8, obsY+app.cellHeight/2, obsX+app.cellWidth/2, obsY, obsX+7*app.cellWidth/8, obsY+app.cellHeight/2, fill='forestGreen', border='white', borderWidth=1.25)
            drawPolygon(obsX+app.cellWidth/6, obsY+app.cellHeight/4, obsX+app.cellWidth/2, obsY, obsX+5*app.cellWidth/6, obsY+app.cellHeight/4, fill='green', border='white', borderWidth=1.25)
        elif obstacle.type == 'tree2':
            drawRect(obsX+4*app.cellWidth/10, obsY+3*app.cellHeight/5, app.cellWidth/5, 2*app.cellHeight/5, fill='brown')
            drawPolygon(obsX+app.cellWidth/8, obsY+4*app.cellHeight/5, obsX+app.cellWidth/2, obsY, obsX+7*app.cellWidth/8, obsY+4*app.cellHeight/5, fill='darkOliveGreen', border='white')
            drawPolygon(obsX+app.cellWidth/6, obsY+app.cellHeight/2, obsX+app.cellWidth/2, obsY, obsX+5*app.cellWidth/6, obsY+app.cellHeight/2, fill='oliveDrab', border='white')
            drawPolygon(obsX+app.cellWidth/4, obsY+app.cellHeight/4, obsX+app.cellWidth/2, obsY, obsX+3*app.cellWidth/4, obsY+app.cellHeight/4, fill='olive', border='white')
        else:
            drawRect(obsX, obsY, app.cellWidth, app.cellHeight, fill='green')

def drawSanta(app):
    cx, cy = app.santaCol*app.cellWidth, app.santaRow*app.cellHeight
    if app.timer % 2 == 0:
        drawImage(app.santaImage1, cx, cy, width=app.santaImageWidth, height=app.santaImageHeight, rotateAngle=-15)
    else:
        drawImage(app.santaImage1, cx, cy, width=app.santaImageWidth, height=app.santaImageHeight, rotateAngle=15)
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
        drawImage(app.giftImageDict[gift.type], x, y, width=app.giftImageWidth, height=app.giftImageHeight, align='center')
        #drawLabel(gift.type, x, y)
    
    drawCircle(app.trashX, app.trashY, 30, align='center', fill='gray')
    drawLabel('Trash Can', app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2)

def drawGiftRequests(app):
     if app.screen == 'default-screen':
        for house in app.houses:
            if house.gift != None:
                labelX, labelY = (house.col+1)*app.cellWidth+app.cellWidth/2, (house.row-1)*app.cellHeight+app.cellHeight/3
                gift = app.giftImageDict[house.gift]
                drawCircle(labelX, labelY+2, 22, border='black', fill='lightgray', opacity=65)
                drawCircle(labelX-app.cellWidth/8, labelY + 9*app.cellHeight/10, 10, border='black', fill='lightgray', opacity=65)
                drawCircle(labelX-app.cellWidth/3, labelY + 1.25*app.cellHeight, 5, border='black', fill='lightgray', opacity=65)
                drawImage(gift, labelX, labelY+2, width=app.giftImageWidth/2, height=app.giftImageHeight/2, align='center')
    
def drawExtraDefault(app):
    drawLabel(f'Level: {app.level}', app.boardWidth/6, app.boardHeight + app.bottomHeight/2, size=20)
    drawLabel(f"Press 'g' to make gifts!", app.boardWidth/2, app.boardHeight + app.bottomHeight/2, size=16)
    drawTimer(app)

    drawLine(0, app.boardHeight, app.boardWidth, app.boardHeight)

def drawTimer(app):
    drawLabel(f'Time: {app.gameTimer} s', 5*app.boardWidth/6, app.boardHeight + app.bottomHeight/2, size=20)

## Gift page
def setUpMaterials(app):
    for i in range(len(app.materialsList)):
        x, y = 35+((app.boardWidth-150)/len(app.materialsList))*i, app.boardHeight+app.bottomHeight/2
        app.materialsBar.append(Material(i, x, y, app.materialsList[i]))

def setUpTools(app):
    #x, y, hitbox radius, type, width, height
    oven = Tool(app.boardWidth-160, app.boardHeight-160, 50, 'oven', 250, 250)
    app.tools['oven'] = oven

    hammer = Tool(50, 50, 30, 'hammer', 80, 80)
    app.tools['hammer'] = hammer

    glue = Tool(50, app.boardHeight-100, 30, 'glue', 65, 65)
    app.tools['glue'] = glue

    knit = Tool(app.boardWidth-100, 70, 30, 'knit', 80, 60)
    app.tools['knit'] = knit

def resetMaterials(app):
    ### resets the indeces for both the materials array and the materialsDictionary that keeps track of the locations
    app.materialsDict = dict()
    for i in range(len(app.materials)):
        material = app.materials[i]
        material.number = i
        app.materialsDict[material.number] = (material.x, material.y)

def resetTools(app):
    for tool in app.tools:
        app.tools[tool].x = app.tools[tool].startX
        app.tools[tool].y = app.tools[tool].startY

def redrawGifts(app):
    drawTools(app)
    drawInventory(app)
    drawMaterials(app)
    drawExtraGifts(app)
    drawHints(app)
    if app.showRecipeBook:
        drawRecipeBook(app)

def drawHints(app):
    drawLabel('Place the right materials, and then use a tool to build a gift!', app.boardWidth/2, 20, size=12, align='center')
    drawLabel("Press 'h' to show/hide recipes", app.boardWidth/2, 40, size=12, align='center')

def drawTools(app):
    drawToolHitboxes(app)
    for tool in app.tools:
        image = app.toolImageDict[tool]
        drawImage(image, app.tools[tool].x, app.tools[tool].y, width=app.tools[tool].width, height=app.tools[tool].height, align='center')

def drawToolHitboxes(app):
    for tool in app.tools:
        cx, cy = app.tools[tool].x, app.tools[tool].y
        drawCircle(cx, cy, app.tools[tool].hitR, fill=None)

def drawMaterials(app):
    for material in app.materials:
        drawImage(app.materialImageDict[material.type], material.x, material.y, width=app.materialImageWidth, height=app.materialImageHeight, align='center')
        #drawCircle(material.x, material.y, material.hitR, fill='gray')
        #drawLabel(f'{material.type}', material.x, material.y)

def drawExtraGifts(app):
    drawLine(0, app.boardHeight, app.boardWidth, app.boardHeight)
    drawTimer(app)
    for i in range(len(app.materialsBar)):
        material = app.materialsBar[i]
        cx, cy = material.x, material.y
        drawImage(app.materialImageDict[material.type], material.x, material.y, width=app.materialImageWidth, height=app.materialImageHeight, align='center')
        #drawCircle(cx, cy, material.hitR, fill='gray')
        #drawLabel(f'{material.type}', cx, cy)

def drawRecipeBook(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=90)
    drawRect(app.width/2, app.height/2, app.recipeWidth, app.recipeHeight, fill='white', align='center')
    drawLabel('Recipes', app.width/2, app.height/8+20, size=20, align='center')
    
    i = 1
    for recipe in app.recipes:
        #drawLabel(f'{recipe}:', app.width/8+100, app.height/8+10+50*i, size=15, bold=True, align='right')
        gift = app.giftImageDict[recipe]
        drawImage(gift, app.width/8+80, app.height/8+10+60*i, width=app.giftImageWidth, height=app.giftImageHeight, align='right')

        j = 1
        for material in app.recipes[recipe]:
            if material != 'tool':
                count = app.recipes[recipe][material]
                image = app.materialImageDict[material]
                drawLabel(f'{count} x ', app.width/8+50+100*j, app.height/8+10+60*i, size=15)
                drawImage(image, app.width/8+60+100*j, app.height/8+10+60*i, width=app.materialImageWidth, height=app.materialImageHeight, align='left')
            else:
                tool = app.recipes[recipe][material]
                image = app.toolImageDict[tool]
                drawImage(image, app.width/2+3*app.width/8-10, app.height/8+10+60*i, width=app.materialImageWidth, height=app.materialImageHeight, align='right')
            j+=1
        i+=1 

### Gift Making
def checkMaterials(app, tool): ### This function checks which materials are overlapping and if they form a recipe
    possibleRecipe = dict()
    overlappingMaterials = []
    seen = set()
    ### Find what materials overlap with the tool
    for material in app.materials:
        cx, cy = material.x, material.y
        if distance(tool.x, tool.y, cx, cy,) < tool.hitR:
            overlappingMaterials.append(material.number)
            possibleRecipe['tool'] = tool.type
    
    if len(overlappingMaterials) > 0:
        tool.x, tool.y = tool.startX, tool.startY

    ### check if materials are all overlapping
    for material1Num in overlappingMaterials:
        for material2Num in overlappingMaterials:
            if material1Num != material2Num:
                material1, material2 = app.materials[material1Num], app.materials[material2Num]
                if distance(material1.x, material1.y, material2.x, material2.y) < material1.hitR + material2.hitR and (material1Num not in seen):
                    seen.add(material1Num)
                    possibleRecipe[material1.type] = possibleRecipe.get(material1.type, 0)+1

    for gift in app.recipes:
        if app.recipes[gift] == possibleRecipe:
            addGift(app, gift)
            for materialNum in reversed(overlappingMaterials): ### reversed prevents the indexing from messing up after popping
                app.materials.pop(materialNum)
            overlappingMaterials, seen = [], set()


def addGift(app, gift):
    if len(app.inventoryList) < app.maxGifts:
        app.inventoryList.append(gift)
        setUpInventory(app)
        resetTools(app)

def main():
    runApp(800, 700)
main()