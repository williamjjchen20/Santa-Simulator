from cmu_graphics import *
import random

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
        self.hitR = 25

    def __repr__(self):
        return self.type

class Material:
    def __init__(self, number, x, y, type):
        self.number = number
        self.x = x
        self.y = y
        self.type = type
        self.hitR = 25

    def __repr__(self):
        return self.type

class Tool:
    def __init__(self, x, y, hitR, type, width, height, angle):
        self.x = x
        self.y = y
        self.startX = x
        self.startY = y
        self.hitR = hitR
        self.type = type
        self.width = width
        self.height = height
        self.angle = angle
    
    def __repr__(self):
        return self.type