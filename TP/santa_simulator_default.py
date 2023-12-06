from santa_simulator_board1 import *
from santa_simulator_images import * 
from santa_simulator_classes import *

from cmu_graphics import *
from PIL import Image
import random

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def resetApp(app, level, totalGifts, resetGame):
    app.totalResets = 0
    app.screen = 'default-screen'
    app.level = level

    app.totalGifts = totalGifts
    app.stepsPerSecond = 10

    app.nextLevel = False
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

    ### Santa
    app.santaRow = 0
    app.santaCol = 0
    app.santaX = app.cellWidth/2
    app.santaY = app.cellHeight/2
    app.santaMoving = False
    app.santaFrame = 0
    app.santaFlip = False
    app.footprints = []

    ## House Finding
    app.path = None
    app.showPath = False
    app.pathTime = None
    app.selectedHouse = None
    app.closestDist = None

    ### Setup Board
    numObstacles = 50+10*app.level
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
        app.recipeWidth, app.recipeHeight = app.width, 3*app.height/4
        app.workbenchY = app.boardHeight/2+275
        app.workbenchHeight = 450

        app.fireFrame = 0

        app.toolAnimation = None
        app.toolTime = None
        app.angleChange = -5
        app.makingGift = False

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
        app.trashX, app.trashY = app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2
        app.gameTimer = 300
        app.timer = 0

        ### Extra features
        app.snow = []
        app.snowTimer = 0
        initSnow(app)

    ### Images
    app.santaImageWidth, app.santaImageHeight = 1.5*app.cellWidth, 1.5*app.cellHeight
    app.houseImageWidth, app.houseImageHeight = 1.3*app.cellWidth, app.cellHeight
    app.materialImageWidth, app.materialImageHeight = 50, 50
    app.giftImageWidth, app.giftImageHeight = 60, 60

    ### Animation
    resetDeliveryAnimation(app)

def chooseBoardDimensions(app, level):
    app.rows = 11 + level
    app.cols = 11 + level
    
def resetBoard(app, numHouses, numObstacles):
    if numObstacles > (app.rows)*(app.cols):
        numObstacles = (app.rows)*(app.cols)//3

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
        app.totalResets += 1

       # print(app.totalResets)

        if app.totalResets > 40:
            resetBoard(app, numHouses, 1)
            return
        if app.resetCounter > 5:
            app.resetCounter = 0
            resetBoard(app, numHouses, numObstacles - 5) 
        else:
            resetBoard(app, app.numHouses, numObstacles)
    print(numObstacles)
    app.resetCounter, app.totalResets = 0, 0
        
def onAppStart(app):
    app.resetCounter, app.totalResets = 0, 0
    resetApp(app, 5, 0, True)

### Maze generation
def isLegalBoard(app):
    for house in app.houses:
        moves = []
        possible = checkLegality(app, house.row, house.col, moves)
        if not possible:
            return False
    return True


def checkLegality(app, row, col, moves): ## I need this function for maze generation because using find path will crash my compter
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
    ###General functions
    app.timer += (1/app.stepsPerSecond)
    if not app.gameOver:
        if app.gameTimer <= 0:
            app.gameOver = True
        if not app.paused:
            app.gameTimer -= (1/app.stepsPerSecond)

    ###Showing path
    if app.pathTime != None:
        if app.timer - app.pathTime > 2:
            app.showPath = False
            app.selectedHouse = None
            app.path = None

    ### Gift delivery
    if app.giftAnimation:
        app.giftAnimationY += 2
        if app.giftAnimationY >= app.giftAnimationYf:
            resetDeliveryAnimation(app)
            if app.nextLevel:
                nextLevel(app)

    ###Snow
    if len(app.snow) < 50 and math.floor(app.timer - app.snowTimer) == 1:
        app.snowTimer = app.timer
        initSnow(app)

    for snow in app.snow:
        dx = random.randint(-1, 1)
        dy = random.randint(1, 5)
        snow.x += dx
        snow.y += dy
        if (snow.x > app.boardWidth or snow.x < 0) or snow.y > app.boardHeight:
            snow.x = random.randint(0, app.boardWidth)
            snow.y = 0
            snow.radius = random.randint(1, 5)

    ### Footprints
    if len(app.footprints) == 6 or not app.santaMoving:
        app.footprints = app.footprints[2:]

    ### Tool Animation
    if app.toolAnimation != None:
        checkMaterials(app, app.tools[app.toolAnimation])
        toolAnimation(app, app.toolAnimation)
    

    ### Fireplace animation
    if app.screen == 'gifts-screen':
        app.fireFrame += 1



def onMousePress(app, mouseX, mouseY):
    #Checks which gift is selected
    if not app.paused:
        for gift in app.inventory:
            if distance(mouseX, mouseY, gift.x, gift.y)<25:
                app.selectedGift = gift.number
                
        if app.screen == 'default-screen':
            for house in app.houses:
                if 0 < mouseX < app.boardWidth and 0 < mouseY < app.boardHeight:
                    mouseRow, mouseCol = getCell(app, mouseX, mouseY)
                    if distance(mouseRow, mouseCol, house.row, house.col) == 0:
                        moves = []
                        #direction = chooseDirection(app.santaRow, app.santaCol, house.row, house.col)
                        path = findPath(app, house.row, house.col, app.santaRow, app.santaCol, moves)
                        
                        if path == 'crashed':
                            print(path)

                        app.resetCounter = 0
                        if path != None and path != 'crashed':
                            path = correctPath(path)
                            #path = list(reversed(path))
                            app.path, app.showPath, app.pathTime = path, True, app.timer
                            app.selectedHouse = house
                        #print(path)

        if app.screen == 'gifts-screen':
            if len(app.materials) < app.maxMaterials:
                for materialIcon in app.materialsBar:
                    if distance(mouseX, mouseY, materialIcon.x, materialIcon.y)<materialIcon.hitR and not app.makingGift:
                        newMaterial = Material(len(app.materials), mouseX, mouseY, materialIcon.type)
                        app.materials.append(newMaterial)

            for material in app.materials:
                if distance(mouseX, mouseY, material.x, material.y)<material.hitR and app.selectedTool == None and not app.makingGift:
                    app.selectedMaterial = material.number
            
            for tool in app.tools:
                x, y = app.tools[tool].x, app.tools[tool].y
                if distance(mouseX, mouseY, x, y) < app.tools[tool].hitR and app.selectedMaterial == None and tool != 'oven' and tool != app.toolAnimation:
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
                        app.inventoryList.pop(gift.number)
                        app.inventory.pop(gift.number)
                        app.selectedGift = None
                        house.gift = None
                        app.giftsDelivered += 1
                        app.totalGifts += 1
                        deliveryAnimation(app, gift, house)
                        if app.giftsDelivered == app.numHouses:
                            app.nextLevel = True
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
            oven = app.tools['oven']
            material = app.materials[app.selectedMaterial]
            if (mouseX > 0 and mouseX < app.boardWidth-material.hitR) and (mouseY > app.workbenchY-app.workbenchHeight/2 and mouseY < app.workbenchY-100):
                material.x, material.y = mouseX, mouseY
                app.materialsDict[material.number] = (material.x, material.y)
                ### special case for the oven
            elif distance(mouseX, mouseY, oven.x, oven.y) < oven.hitR:
                checkMaterials(app, oven)
                # app.toolAnimation = 'oven'
                # app.toolTime = app.timer
            else:
                app.materials.pop(material.number)
                resetMaterials(app)
            app.selectedMaterial = None
            #checkMaterials(app)

        if app.selectedTool != None and app.screen == 'gifts-screen':
            tool = app.tools[app.selectedTool]
            if (mouseX > 0 and mouseX < app.boardWidth-tool.hitR) and (mouseY > 0 and mouseY < app.boardHeight-tool.hitR):
                tool.x, tool.y = mouseX, mouseY
                checkMaterials(app, tool)
                # app.toolAnimation = tool.type
                # app.toolTime = app.timer
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

    if key == 'r' and not app.gameStart: ### Restart game 
        resetApp(app, 1, 0, True)

    if not app.gameOver:   
        if not app.paused:
            if key == 'g':
                if app.screen == 'default-screen':
                    app.screen = 'gifts-screen'
                elif app.screen == 'gifts-screen':
                    app.screen = 'default-screen'

            if key == 'h' and app.screen == 'gifts-screen':
                app.showRecipeBook = not app.showRecipeBook

            app.showPath = False
            
def onKeyHold(app, keys):
    if not app.gameOver:   
        if not app.paused:
            oldX, oldY = app.santaX, app.santaY
            dx, dy = None, None
            changeX, changeY = app.cellWidth/4, app.cellHeight/4
            if 'right' in keys: 
                app.santaX += changeX
                dx, dy = changeX, 0
            elif 'left' in keys: 
                app.santaX -= changeX
                dx, dy = -changeX, 0
            elif 'down' in keys: 
                app.santaY += changeY
                dx, dy = 0, changeY
            elif 'up' in keys:
                app.santaY -= changeY
                dx, dy = 0, -changeY

            if dx != None and dy != None:
                app.santaFrame += 1
                if dx < 0:
                    app.santaFlip = True
                elif dx > 0:
                    app.santaFlip = False
            moveCheck(app, dx, dy)

            ### Set up footprints
            if app.santaX != oldX or app.santaY != oldY:
                if abs(dx) > 0:
                    app.footprints.append((oldX, oldY+app.cellHeight/2 - 3, 'horizontal'))
                    app.footprints.append((oldX, oldY+app.cellHeight/2, 'horizontal'))
                elif abs(dy) > 0:
                    app.footprints.append((oldX + 3, oldY, 'vertical'))
                    app.footprints.append((oldX, oldY, 'vertical'))
            
            app.santaRow, app.santaCol = getCell(app, app.santaX, app.santaY)
            app.santaMoving = True
            
def onKeyRelease(app, key):
    if key == 'right' or key == 'left' or key == 'up' or key == 'down':
        app.santaMoving = False

def moveCheck(app, dx, dy):
    xleft, xright = math.ceil(app.santaX - app.cellWidth/2), math.floor(app.santaX + app.cellWidth/2)
    ytop, ybot = math.ceil(app.santaY - app.cellHeight/2), math.floor(app.santaY + app.cellHeight/2)
    if ybot > app.boardHeight or ytop < 0:
        app.santaY -= dy
    elif xright > app.boardWidth or xleft < 0:
        app.santaX -= dx
    else:
        app.santaRow, app.santaCol = getCell(app, app.santaX, app.santaY)
        if app.board[app.santaRow][app.santaCol] == 'house' or app.board[app.santaRow][app.santaCol] in app.obstacleTypes:
            if dx == 0:
                app.santaY -= dy
            elif dy == 0:
                app.santaX -= dx

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

def nextLevel(app):
    resetApp(app, app.level+1, app.totalGifts, False)
    app.giftsDelivered = 0 
    generateGifts(app, 0)

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
    drawRect(app.width/2-15, app.height/2-75, 20, 50, fill='white', align='center')
    drawRect(app.width/2+15, app.height/2-75, 20, 50, fill='white', align='center')
    drawLabel('Game Paused', app.width/2, app.height/2, fill='white', size=50, bold=True, align='center')
    drawLabel("Press 'space' to resume", app.width/2, app.height/2+50, fill='white', size=20, align='center')
    drawLabel("Press 'r' to restart", app.width/2, app.height/2+75, fill='white', size=20, align='center')

def drawStartScreen(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    titleColor = 'red' if math.floor(app.timer) % 2 == 0 else 'green'
    labelColor = 'green' if math.floor(app.timer) % 2 == 0 else 'red'
    drawLabel('Santa Simulator', app.width/2, app.height/4, fill=titleColor, size=50, bold=True, align='center')
    drawLabel('Press space to start game!', app.width/2, app.height/4+50, fill=labelColor, italic=True, size=25, align='center')

    drawLabel('As Santa, your job is to deliver gifts to everyone this Christmas.', app.width/2, app.height/2, size=15)
    drawLabel('Sadly, your sleigh broke down, so you must reach each house on foot.', app.width/2, app.height/2 + 20, size=15)
    drawLabel('Make sure to craft the right gift in the workshop!', app.width/2, app.height/2 + 40, size=15)

    drawLights(app)

def drawLights(app):
    colors = ['lightgreen', 'red', 'pink', 'yellow', 'orange']
    lightSpacing = app.width/10
    for cx in range(10):
        drawOval(cx*lightSpacing+lightSpacing/2, 0, lightSpacing, 50, fill=None, border='black')
        randColor = random.randint(0, len(colors)-1)
        drawCircle(cx*lightSpacing+lightSpacing/2, 25, 10, fill=colors[randColor], border=None)
        drawCircle(cx*lightSpacing+lightSpacing/2+4, 20, 3, fill='white', border=None)
        drawCircle(cx*lightSpacing+lightSpacing/2+5, 26, 1.2, fill='white', border=None)


def drawGameOver(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=90)
    color1 = 'red' if app.timer % 2 == 0 else 'green'
    color2 = 'green' if app.timer % 2 == 0 else 'red'
    drawLabel('Times Up!', app.width/2, app.height/2, size=50, fill=color1, bold=True, align='center')
    drawLabel(f'Gifts Delivered: {app.totalGifts}', app.width/2, app.height/2 + 50, fill=color2, size=20, align='center')

    drawLabel("Press 'space' to restart", app.width/2, app.height/2 + 150, fill='white', size=20, align='center')

def drawGameComplete(app):
    drawRect(0, 0, app.width, app.height, fill='white')
    color1 = 'red' if math.floor(app.timer) % 2 == 0 else 'green'
    color2 = 'green' if math.floor(app.timer) % 2 == 0 else 'red'
    drawLabel('Great Work, Santa!', app.width/2, app.height/2, size=50, fill=color1, bold=True, align='center')
    drawLabel(f'Gifts Delivered: {app.totalGifts}', app.width/2, app.height/2 + 50, fill='black', size=20, align='center')
    drawLabel(f'Time Elapsed: {math.floor(300-app.gameTimer)} seconds', app.width/2, app.height/2 + 75, fill='black', size=20, align='center')

    drawLabel("Press 'space' or 'r' to play again", app.width/2, app.height/2 + 150, fill=color2, size=20, align='center')

    drawLights(app)

## Main Page
def redrawDefault(app):
    #drawBoard(app)
    drawHouses(app)
    drawObstacles(app)
    drawSanta(app)
    drawInventory(app)
    drawGiftRequests(app)
    drawExtraDefault(app)
    drawAnimations(app)

###
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*1)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=1)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
###


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
    if obsPos == 0 and (obsRow, obsCol) != (app.santaRow, app.santaCol):
        app.board[obsRow][obsCol] = app.obstacleTypes[randObs]
    else:
        generateObstacle(app, i)
        return
    app.obstacles.append(Obstacle(i, obsRow, obsCol, app.obstacleTypes[randObs]))
    
def isClogged(app, row, col):
    for house in app.houses:
        dist = ((row-house.row)**2 + (col-house.col)**2)**0.5
        if dist <= 3:
            return True 
    return False

def drawHouses(app):
    housePics = [app.houseImage1, app.houseImage2, app.houseImage3]
    for house in app.houses:
        houseX, houseY = house.col*app.cellWidth, house.row*app.cellHeight
        drawImage(housePics[house.number%len(housePics)], houseX+app.cellWidth/2, houseY+app.cellHeight/2 + 2, width=app.houseImageWidth, height=app.houseImageHeight, align='center')
        drawOval(houseX+app.cellWidth/2, houseY+app.cellHeight, 3*app.cellWidth/4, app.cellHeight/5, fill='gray', opacity=30)

def drawObstacles(app):
    for obstacle in app.obstacles:
        obsX, obsY = obstacle.col*app.cellWidth, obstacle.row*app.cellHeight

        ###animate the trees
        obsX, obsY = animateTrees(app, obstacle, obsX, obsY)
        
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
        # else:
        #     drawRect(obsX, obsY, app.cellWidth, app.cellHeight, fill='green')

def drawSanta(app):
    cx, cy = app.santaX, app.santaY

    santaImage = app.santaImages[app.santaFrame%len(app.santaImages)]


    if app.santaFlip:
        santaImage = app.santaImagesFlipped[app.santaFrame%len(app.santaImages)]

    if not app.santaMoving:
        if not app.santaFlip:
            santaImage = app.santaImages[2]
        else:
            santaImage = app.santaImagesFlipped[2]
    
    santaImage = CMUImage(santaImage)

    for (footX, footY, orientation) in app.footprints:
        if orientation == 'horizontal':
            drawOval(footX, footY, 5, 2, opacity=30)
        elif orientation == 'vertical':
            drawOval(footX, footY, 2, 5, opacity=30)

    if (math.floor(app.timer)) % 2 == 0:
        drawImage(santaImage, cx, cy, width=app.santaImageWidth, height=app.santaImageHeight, rotateAngle=-15, align='center')
    else:
        drawImage(santaImage, cx, cy, width=app.santaImageWidth, height=app.santaImageHeight, rotateAngle=15, align='center')
    #drawCircle(cx, cy, 10, fill='blue', align='center')

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
    drawRect(app.boardWidth, 0, app.inventoryWidth, app.height, fill= 'white' if app.screen=='default-screen' else'blanchedalmond')
    drawLine(app.boardWidth, 0, app.boardWidth, app.height)
    drawLabel('Gifts', app.boardWidth+app.inventoryWidth/2, 20, align='center', size=20)

    for i in range(len(app.inventoryList)):
        gift = app.inventory[i]
        x, y = gift.x, gift.y
        drawImage(app.giftImageDict[gift.type], x, y, width=app.giftImageWidth, height=app.giftImageHeight, align='center')
        #drawLabel(gift.type, x, y)
    
    drawImage(app.trashImage, app.trashX, app.trashY, width=60, height=60, align='center')
    #drawCircle(app.trashX, app.trashY, 30, align='center', fill='gray')
    #drawLabel('Trash Can', app.boardWidth+app.inventoryWidth/2, app.boardHeight+app.bottomHeight/2)

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

    ### draw path
    if app.showPath:
        showPath(app)

def drawTimer(app):
    drawLabel(f'Time: {math.floor(app.gameTimer)} s', 5*app.boardWidth/6, app.boardHeight + app.bottomHeight/2, size=20)

## Gift page
def setUpMaterials(app):
    for i in range(len(app.materialsList)):
        x, y = 35+((app.boardWidth-150)/len(app.materialsList))*i, app.boardHeight
        app.materialsBar.append(Material(i, x, y, app.materialsList[i]))

def setUpTools(app):
    #x, y, hitbox radius, type, width, height, angle
    oven = Tool(app.boardWidth-175, app.boardHeight/2-100, 60, 'oven', 300, 300, 0)
    app.tools['oven'] = oven

    hammer = Tool(50, 60, 30, 'hammer', 80, 80, -15)
    app.tools['hammer'] = hammer

    glue = Tool(50, 205, 30, 'glue', 65, 65, 15)
    app.tools['glue'] = glue

    knit = Tool(125, 140, 30, 'knit', 80, 60, 30)
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
    drawBackDrop(app)
    drawTools(app)
    drawInventory(app)
    drawMaterials(app)
    drawExtraGifts(app)
    drawHints(app)
    if app.showRecipeBook:
        drawRecipeBook(app)
    drawAnimations(app)

def drawBackDrop(app):
    drawRect(0, 0, app.boardWidth, app.boardHeight-100, fill='bisque')
    drawRect(0, app.boardHeight/2, app.boardWidth, app.boardHeight, fill='tan')
    ###shelf
    shelfX, shelfY = app.boardWidth/2-200, app.boardHeight/2-125
    drawOval(shelfX, shelfY + 150, 250, 30, fill='black', opacity=40)
    drawImage(app.shelfImage, shelfX, shelfY, width=200, height=300, align='center')

    drawImage(app.workbenchImage, app.boardWidth/2, app.workbenchY, width=1.2*app.boardWidth, height=app.workbenchHeight, align='center')
    drawImage(app.tableImage, app.boardWidth/2-25, app.boardHeight+25, width=1.2*app.boardWidth, height=app.boardHeight, align='center')

    fillGaps(app)

def fillGaps(app):
    drawLine(0, 537.5, 515, 537.5, fill='tan', lineWidth=3)
    drawLine(85, 503, 515, 503, fill='tan', lineWidth=7)
    drawLine(520, 538, app.boardWidth, 636, fill='tan', lineWidth=2)
    drawLine(0, 395, 47, 347, fill='tan', lineWidth=4)
    drawLine(app.boardWidth, 395, 551, 347, fill='tan', lineWidth=4)
    drawLine(515, 500, 515, 538, fill='tan', lineWidth=3)
    drawLine(553, 500, 553, 578, fill='tan', lineWidth=5)

def drawHints(app):
    drawLabel('Place the right materials, and then use a tool to build a gift!', app.boardWidth/2, 15, size=12, align='center')
    drawLabel("Press 'h' to show/hide recipes", app.boardWidth/2, 40, size=12, align='center')

def drawTools(app):
    drawToolHitboxes(app)
    for toolType in app.tools:
        tool = app.tools[toolType]
        image = app.toolImageDict[toolType]
        cx, cy, rx, ry = tool.x, tool.y+tool.hitR, 3*tool.hitR, tool.hitR/2
        if toolType == 'oven':
            cy = tool.y+2*tool.hitR
            rx = 3.5*tool.hitR
            drawOval(cx, cy, rx, ry, fill='black', opacity=40)
            fireImage = app.fireImages[app.fireFrame%len(app.fireImages)]
            drawRect(tool.x, tool.y+60, 100, 100, align='center', fill=rgb(95, 40, 15), opacity=80)
            drawImage(image, tool.x, tool.y, width=tool.width, height=tool.height, rotateAngle=tool.angle, align='center')
            drawImage(fireImage, tool.x, tool.y+50, width=150, height=150, align='center')
        else:
            drawOval(cx, cy, rx, ry, fill='black', opacity=40)
            drawImage(image, tool.x, tool.y, width=tool.width, height=tool.height, rotateAngle=tool.angle, align='center')
        
        if app.toolAnimation != None:
            tool = app.tools[app.toolAnimation]
            drawLabel("Crafting...", tool.x, tool.y-50, align='center', fill='white', italic=True, size=20)

def drawTool(app, tool):
    image = app.toolImageDict[tool.type]
    drawImage(image, tool.x, tool.y, width=tool.width, height=tool.height, rotateAngle=tool.angle, align='center')

def drawToolHitboxes(app):
    for tool in app.tools:
        cx, cy = app.tools[tool].x, app.tools[tool].y
        drawCircle(cx, cy, app.tools[tool].hitR, fill=None)

def drawMaterials(app):
    for material in app.materials:
        drawOval(material.x, material.y+3*material.hitR/4, 2*material.hitR, material.hitR, fill='black', opacity=30)
        drawImage(app.materialImageDict[material.type], material.x, material.y, width=app.materialImageWidth, height=app.materialImageHeight, align='center')
        #drawCircle(material.x, material.y, material.hitR, fill='gray')
        #drawLabel(f'{material.type}', material.x, material.y)

def drawExtraGifts(app):
    drawTimer(app)
    for i in range(len(app.materialsBar)):
        material = app.materialsBar[i]
        drawOval(material.x, material.y+3*material.hitR/4, 2*material.hitR, material.hitR, fill='black', opacity=30)
        drawImage(app.materialImageDict[material.type], material.x, material.y, width=app.materialImageWidth, height=app.materialImageHeight, align='center')
        #drawLabel(f'{material.type}', cx, cy)

def drawRecipeBook(app):
    drawRect(0, 0, app.width, app.height, fill='black', opacity=80)
    #drawRect(app.width/2, app.height/2, app.recipeWidth, app.recipeHeight, fill='white', align='center')
    drawImage(app.bookImage, app.width/2, app.height/2, width=app.recipeWidth, height=app.recipeHeight, align='center')
    drawLabel('Recipes', app.width/2, app.height/5, size=30, align='center', bold=True, fill='white')
    
    i = 1
    for recipe in app.recipes:
        materialGap = 70
        firstGap = 20
        recipeGap = 60

        #drawLabel(f'{recipe}:', app.width/8+100, app.height/8+10+50*i, size=15, bold=True, align='right')
        gift = app.giftImageDict[recipe]
        drawImage(gift, app.width/7+firstGap, app.height/8+10+60*i, width=app.giftImageWidth, height=app.giftImageHeight, align='right', opacity=70)

        j = 1
        for material in app.recipes[recipe]:
            if material != 'tool':
                count = app.recipes[recipe][material]
                image = app.materialImageDict[material]
                drawLabel(f'{count} x ', app.width/10+firstGap+materialGap*j, app.height/8+10+recipeGap*i, size=15)
                drawImage(image, app.width/10+firstGap+materialGap*j + 7, app.height/8+10+recipeGap*i, width=app.materialImageWidth, height=app.materialImageHeight, align='left', opacity=70)
            else:
                tool = app.recipes[recipe][material]
                image = app.toolImageDict[tool]
                drawImage(image, app.width/2+3*app.width/8-10, app.height/8+10+recipeGap*i, width=app.materialImageWidth, height=app.materialImageHeight, align='right', opacity=70)
            j+=1
        i+=1 
    
    fillRecipeGaps(app)

def fillRecipeGaps(app):
    drawLine(6, 600, 29, 109, fill=rgb(50, 10, 0), lineWidth=11)
    drawLine(4, 600, 794, 600, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(794, 602, 770, 109, fill=rgb(50, 10, 0), lineWidth=11)
    drawLine(29, 109, 73, 100, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(70, 100, 380, 100, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(378, 100, 400, 108, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(400, 108, 428, 98, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(427, 98, 738, 98, fill=rgb(50, 10, 0), lineWidth=8)
    drawLine(737, 98, 772, 112, fill=rgb(50, 10, 0), lineWidth=8)
    #drawOval(210, 110, 380, 50, borderWidth=10, fill='blue')
    #drawOval(210, 110, 360, 40, fill='black', opacity=0)

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
            if app.toolAnimation == None:
                app.toolAnimation = tool.type
                app.toolTime = app.timer
                app.makingGift = True

            if math.floor(app.timer - app.toolTime) >= 3:
                addGift(app, gift)
                for materialNum in reversed(overlappingMaterials): ### reversed prevents the indexing from messing up after popping
                    app.materials.pop(materialNum)
                    resetMaterials(app)

                overlappingMaterials, seen = [], set()
    if not app.makingGift:
        resetTools(app)
    
def addGift(app, gift):
    if len(app.inventoryList) < app.maxGifts:
        app.inventoryList.append(gift)
        setUpInventory(app)

### Extra Features
    
def showPath(app):
    pathColor = 'black'
    path = app.path[1:]
    for i in range(len(path)):
        row, col = path[i]
        drawCircle(col*app.cellWidth+app.cellWidth/2, row*app.cellHeight+app.cellHeight/2, 10, fill=pathColor, opacity=10)
    
def findPath(app, houseRow, houseCol, santaRow, santaCol, moves):
    app.resetCounter += 1
    print(app.resetCounter)
    if app.resetCounter > 2000:
        return 'crashed'
    if distance(santaRow, santaCol, houseRow, houseCol) == 1:
        moves.append((santaRow, santaCol))
        return moves
    else:
        moves.append((santaRow, santaCol))
        #if santaCol == houseCol or santaRow == houseRow and distance(santaRow, santaCol, houseRow, houseCol) < 5:
        direction = chooseDirection(santaRow, santaCol, houseRow, houseCol)
        for (drow, dcol) in direction:
            if isLegalMove(app, santaRow+drow, santaCol+dcol) and (santaRow+drow, santaCol+dcol) not in moves:
                santaRow += drow
                santaCol += dcol
                solution = findPath(app, houseRow, houseCol, santaRow, santaCol, moves)
                if solution != None:
                    return solution
                elif solution == 'crashed':
                    return 'crashed'
                moves.pop()
                santaRow -= drow
                santaCol -= dcol
        return None

def chooseDirection(row, col, row2, col2):
    bestDirection = None
    diffCol, diffRow = col2-col, row2-row
    
    normDiffCol = int(diffCol/abs(diffCol)) if diffCol != 0 else 0
    normDiffRow = int(diffRow/abs(diffRow)) if diffRow != 0 else 0
    if diffCol == 0:
        bestDirection = [(normDiffRow, 0), (0, normDiffRow), (-normDiffRow, 0), (0, -normDiffRow)]
    elif diffRow == 0:
        bestDirection = [(0, normDiffCol), (normDiffCol, 0), (0, -normDiffCol), (-normDiffCol, 0)]
    elif abs(diffRow) > abs(diffCol):
        bestDirection =  [(normDiffRow, 0), (0, normDiffCol), (-normDiffRow, 0), (0, -normDiffCol)]
    elif abs(diffCol) >= abs(diffRow):
        bestDirection = [(0, normDiffCol), (normDiffRow, 0), (0, -normDiffCol), (-normDiffRow, 0)]

    return bestDirection

def correctPath(path):
    i = 0
    while i < len(path):
        if i > 100:
            return
        (row, col) = path[i]
        largestIndex = None
        for drow, dcol in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if (row+drow, col+dcol) in path:
                i2 = path.index((row+drow, col+dcol))
                if i2 >= i and (largestIndex == None or i2 > largestIndex):
                    largestIndex = i2
        if largestIndex != None:
            path = path[0: i+1] + path[largestIndex:]
        i+=1
    return path

### Animations
def drawAnimations(app):
    if app.screen == 'default-screen' and app.giftAnimation:
        drawGiftFalling(app)
    if app.screen == 'default-screen':
        for snow in app.snow:
            drawSnow(snow)
    if app.screen == 'gifts-screen' and app.toolAnimation != None and app.toolAnimation != 'oven':
        drawTool(app, app.tools[app.toolAnimation])

def animateTrees(app, obstacle, obsX, obsY):
    if obstacle.number % 2 == 0:
        if (math.floor(app.timer)) % 2 == 0:
            obsY -= 1
        else:
            obsY += 1
    elif obstacle.number % 2 == 1:
        if (math.floor(app.timer)) % 2 == 0:
            obsY += 1
        else:
            obsY -= 1

    return obsX, obsY

### Snow
def initSnow(app):
    for i in range(2):
        x = random.randint(0, app.boardWidth)
        y = 0
        radius = random.randint(3, 5)
        snow = Snow(x, y, radius)
        app.snow.append(snow)

def drawSnow(snow):
    drawCircle(snow.x, snow.y, snow.radius, fill='white', border='lightblue')

### Gift Delivery
def resetDeliveryAnimation(app):
    app.giftAnimation = False
    app.giftFallTime = None
    app.giftAnimationType = None
    app.giftAnimationX, app.giftAnimationY = None, None

def deliveryAnimation(app, gift, house):
    app.giftAnimation = True
    app.giftAnimationType = app.giftImageDict[gift.type]
    app.giftAnimationX, app.giftAnimationY = house.col*app.cellWidth+app.cellWidth/2, house.row*app.cellHeight-app.cellHeight
    app.giftAnimationYf = house.row*app.cellHeight + app.cellHeight/2

def drawGiftFalling(app):
    drawImage(app.giftImage, app.giftAnimationX, app.giftAnimationY-5, width=1.2*app.giftImageWidth, height=app.giftImageHeight, align='center')
    #drawCircle(app.giftAnimationX, app.giftAnimationY, app.giftImageWidth/3, fill='white')
    drawImage(app.giftAnimationType, app.giftAnimationX, app.giftAnimationY, width=app.giftImageWidth/2, height=app.giftImageHeight/2, align='center')

### Tool Animations
def toolAnimation(app, tool):
    time = app.timer - app.toolTime
    tool = app.tools[app.toolAnimation]
    if math.floor(time) < 3:
        if tool.type == 'hammer':
            tool.angle += app.angleChange
            if abs(tool.angle) == 30:
                app.angleChange *= -1
        elif tool.type == 'knit':
            if time < 1.5:
                tool.angle -= 2
            else:
                tool.angle += 2
        elif tool.type == 'glue':
            if tool.angle < 180:
                tool.angle += 180
            if time < 1:
                tool.y += 1
                tool.angle -= 1
            elif time > 1 and time < 2:
                tool.y -= 1 
                tool.angle += 1
            elif time > 2:
                tool.angle -= 180
    else:
        app.toolAnimation = None
        app.makingGift = False
        resetTools(app)

### Sparkles
def playSparkles(app):
    pass

def main():
    runApp(800, 700)
main()