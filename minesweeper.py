# Find an image "needle" in another image "haystack" with RMS error less than "tolerance"
# returns location of needle in haystack

import win32gui
import os
import Image
import ImageOps
import ImageGrab
import ImageChops
from autoinput import *
from random import randint
from time import clock
from gamepad import *
from gamepad.events import *

class Minesweeper:
    
    GRID_OFFSET = (15, 116)
    SQUARE_SIZE = (16, 16)
    
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.windowRect = win32gui.GetWindowRect(hwnd)
        fin = open('features.txt')
        self.features = eval(fin.read())

        win32gui.SetForegroundWindow(hwnd)
        self.initializeGrid()
        
        (left, top, right, bottom)  = self.windowRect
        self.gridLeft = left + Minesweeper.GRID_OFFSET[0]
        self.gridTop = top + Minesweeper.GRID_OFFSET[1]
        self.gridRight = self.gridLeft + self.numCols*Minesweeper.SQUARE_SIZE[0]
        self.gridBottom = self.gridTop + self.numRows*Minesweeper.SQUARE_SIZE[0]
        self.gridRect = (self.gridLeft, self.gridTop, self.gridRight, self.gridBottom)
        
        self.updateGrid()
        
    def solve(self):
        grid = self.grid
        rows = self.numRows
        cols = self.numCols
        neighbors = ((-1, -1), (-1, 0), (-1, 1),
                     (0 , -1),          ( 0, 1),
                     (1 , -1), ( 1, 0), ( 1, 1))
        
        unknowns = [None]*rows
        for i in range(0, rows):
            unknowns[i] = [None]*cols
            for j in range(0, cols):
                unknowns[i][j] = []
            
        mines = [0]*rows
        for i in range(0, rows):
            mines[i] = [0]*cols
        
        for i in range(0, rows):
            for j in range(0, cols):
                if grid[i][j] == ' ':
                    for k in range(0, len(neighbors)):
                        ni = i + neighbors[k][0]
                        nj = j + neighbors[k][1]
                        if ni >= 0 and ni < rows and nj >= 0 and nj < cols:
                            unknowns[ni][nj].append((i,j))
                elif grid[i][j] == '*':
                    for k in range(0, len(neighbors)):
                        ni = i + neighbors[k][0]
                        nj = j + neighbors[k][1]
                        if ni >= 0 and ni < rows and nj >= 0 and nj < cols:
                            mines[ni][nj] += 1

        success = False

        # mark
        for i in range(0, rows):
            for j in range(0, cols):
                if len(unknowns[i][j]) > 0 and grid[i][j] == len(unknowns[i][j]) + mines[i][j]:
                    for k in range(0, len(unknowns[i][j])):
                        self.mark(unknowns[i][j][k])
                    success = True

        # sweep
        for i in range(0, rows):
            for j in range(0, cols):
                if not self.sweeped[i][j] and grid[i][j] > 0 and grid[i][j] == mines[i][j]:
                    self.sweep((i, j))
                    success = True
            
        guess = (0,0)
        minUnknown = 8
        if not success:
            for i in range(0, rows):
                for j in range(0, cols):
                    if grid[i][j] != '*' and grid[i][j] != ' ' and grid[i][j] > 0 and len(unknowns[i][j]) > 0 and len(unknowns[i][j]) < minUnknown:
                        minUnknown = unknowns[i][j]
                        guess = (i, j)
            unknown = unknowns[guess[0]][guess[1]]
            if len(unknown) <= 0:
                raise Exception, 'Grid already solved'
            self.clear(unknown[randint(1, len(unknown)) - 1])
            success = True
                    
        return success

    def mark(self, (i, j)):
        if self.grid[i][j] != ' ':
            return
        
        x = self.gridLeft + j*Minesweeper.SQUARE_SIZE[0] + Minesweeper.SQUARE_SIZE[0]/2
        y = self.gridTop + i*Minesweeper.SQUARE_SIZE[1] + Minesweeper.SQUARE_SIZE[1]/2
        Mouse.moveTo(x, y)
        Mouse.click(Mouse.RIGHT)
        self.grid[i][j] = '*'

    def sweep(self, (i, j)):
        x = self.gridLeft + j*Minesweeper.SQUARE_SIZE[0] + Minesweeper.SQUARE_SIZE[0]/2
        y = self.gridTop + i*Minesweeper.SQUARE_SIZE[1] + Minesweeper.SQUARE_SIZE[1]/2
        Mouse.moveTo(x, y)
        Mouse.click(Mouse.LEFT + Mouse.RIGHT)
        self.sweeped[i][j] = True
        
    def clear(self, (i, j)):
        x = self.gridLeft + j*Minesweeper.SQUARE_SIZE[0] + Minesweeper.SQUARE_SIZE[0]/2
        y = self.gridTop + i*Minesweeper.SQUARE_SIZE[1] + Minesweeper.SQUARE_SIZE[1]/2
        Mouse.moveTo(x, y)
        Mouse.click(Mouse.LEFT)
    
    def windowSize(self):
        (left, top, right, bottom)  = self.windowRect
        return (right - left, bottom - top)
        
    def gridDimensions(self):
        (w, h) = (self.windowWidth, self.windowHeight)
        w = w - 15 - 11
        h = h - 116 - 11
        numCols = w / 16
        numRows = h / 16
        return (numRows, numCols)
        
    def initializeGrid(self):
        (self.windowWidth, self.windowHeight) = self.windowSize()
        (self.numRows, self.numCols) = self.gridDimensions()
        
        self.grid = [None]*self.numRows
        for i in range(0, self.numRows):
            self.grid[i] = [' ']*self.numCols
            
        self.sweeped = [None]*self.numRows
        for i in range(0, self.numRows):
            self.sweeped[i] = [False]*self.numCols
            
    def updateGrid(self):
        im = ImageGrab.grab(self.gridRect)
        self.im = im
        
        for i in range(0, self.numRows):
            for j in range(0, self.numCols):
                self.grid[i][j] = self.cellAt((i, j))
                
    def cellAt(self, (i, j)):
        width = self.im.size[0]
        im = self.im.getdata()
        features = self.features
        grid = self.grid
        sw = Minesweeper.SQUARE_SIZE[0]
        sh = Minesweeper.SQUARE_SIZE[1]
        
        # do color checking on numbers 1 - 9
        for num in range(1, 9):
            (color, location) = features[num]
            x = j*sw + location[0]
            y = i*sh + location[1]

            if im[width*y + x] == color:
                return num

        cellTypes = ('*', 0, ' ')
        for cellType in cellTypes:
            (color, location) = features[cellType]
            x = j*sw + location[0]
            y = i*sh + location[1]

            if im[width*y + x] == color:
                return cellType
                
        raise Exception, 'Cannot determine type of cell at (%d, %d)' % (i, j)

def find(haystack, needle, tolerance = 100):
    return (-1, -1)

def gridSize(windowSize):
    (w, h) = windowSize
    w = w - 15 - 11
    h = h - 116 - 11
    width = w / 16
    height = h / 16
    return (width, height)
    
    
hwnd = win32gui.FindWindow(None, 'Minesweeper')

# win32gui.ShowWindow
# 0 - hide
# 1 - unhide
# 2 - minimize
# 3 - maximize
# 4 - restore

#win32gui.ShowWindow(hwnd, 4)
#win32gui.SetActiveWindow(hwnd)
#win32gui.SetFocus(hwnd)

# get bounding box (left, top, right, bottom)
#boundingBox = win32gui.GetWindowRect(hwnd)
#im = ImageGrab.grab(boundingBox)
#im.save('temp.png')
#im = Image.open('temp.png')
#gridSize2(im)
#os.remove('temp.png')

if hwnd == 0:
    print 'Minesweeper not running'
    quit()

(left, top, right, bottom) = win32gui.GetWindowRect(hwnd)

print gridSize((right - left, bottom - top))

minesweeper = Minesweeper(hwnd)

# test.py

updateTimes = []
solveTimes = []

def solve(gamepad):
    if gamepad.buttonState(3): # Square
        t = clock()
        minesweeper.updateGrid()
        updateTimes.append(clock() - t)
        t = clock()
        
        if not minesweeper.solve():
            gamepad.stop()
            
        solveTimes.append(clock() - t)

def reset(gamepad, event):
    if event.buttonIndex == 7: # R1
        Keyboard.press(Keyboard.VirtualKeys.F2)
        
def stop(gamepad):
    shouldStop = True
    for btn in [4,5,6,7]:
        shouldStop &= gamepad.buttonState(btn)
    if shouldStop:
        gamepad.stop()

g = Gamepad()            
g.addGamepadCallback(solve)
g.addEventHandler(ButtonPressedEvent, reset)
g.addGamepadCallback(stop)
g.start()

print 'Press L1,L2,R1,R2 on gameController to stop'
print 'Hold square [] on gameController to play'
g.join()

updateTimeTotal = sum(updateTimes)
solveTimeTotal = sum(solveTimes)
timeTotal = updateTimeTotal + solveTimeTotal
print 'Total time: %.1f seconds' % timeTotal
print 'Update time:'
print '\t%.1f%%\tavg:%.1f ms' % (100.0*updateTimeTotal / timeTotal, 1000.0*updateTimeTotal/len(updateTimes))
print 'Solve time:'
print '\t%.1f%%\tavg:%.1f ms' % (100.0*solveTimeTotal / timeTotal, 1000.0*solveTimeTotal/len(solveTimes))

