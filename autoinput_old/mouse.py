from ctypes import *
from structs import *
from interop import *

class Mouse():

    # constants
    XBUTTON1 = 0x0001;
    XBUTTON2 = 0x0002;
    MOUSEEVENTF_MOVE = 0x0001;
    MOUSEEVENTF_LEFTDOWN = 0x0002;
    MOUSEEVENTF_LEFTUP = 0x0004;
    MOUSEEVENTF_RIGHTDOWN = 0x0008;
    MOUSEEVENTF_RIGHTUP = 0x0010;
    MOUSEEVENTF_MIDDLEDOWN = 0x0020;
    MOUSEEVENTF_MIDDLEUP = 0x0040;
    MOUSEEVENTF_XDOWN = 0x0080;
    MOUSEEVENTF_XUP = 0x0100;
    MOUSEEVENTF_WHEEL = 0x0800;
    MOUSEEVENTF_VIRTUALDESK = 0x4000;
    MOUSEEVENTF_ABSOLUTE = 0x8000;
    WHEEL_DELTA = 120;
    
    LEFT = MOUSEEVENTF_LEFTDOWN
    RIGHT = MOUSEEVENTF_RIGHTDOWN
    MIDDLE = MOUSEEVENTF_MIDDLEDOWN
    NUMBUTTONS = 3

    # structures to pass to SendInput (preinitialized for efficiency)
    
    moveInput = INPUT()
    moveInput.type = INPUT.MOUSE
    moveInput.mi.dwFlags = MOUSEEVENTF_MOVE
    moveInput.mi.dwExtraInfo = 0
    moveInput.mi.mouseData = 0
    moveInput.mi.time = 0
    
    moveToInput = INPUT()
    moveToInput.type = INPUT.MOUSE
    moveToInput.mi.dwFlags = MOUSEEVENTF_ABSOLUTE + MOUSEEVENTF_MOVE
    moveToInput.mi.dwExtraInfo = 0
    moveToInput.mi.mouseData = 0
    moveToInput.mi.time = 0
    
    clickInput = INPUT()
    clickInput.type = INPUT.MOUSE;
    clickInput.mi.dwExtraInfo = 0;
    clickInput.mi.mouseData = 0;
    clickInput.mi.time = 0;
    
    scrollInput = INPUT()
    scrollInput.type = INPUT.MOUSE;
    scrollInput.mi.dwFlags = MOUSEEVENTF_WHEEL;
    scrollInput.mi.dwExtraInfo = 0;
    scrollInput.mi.time = 0;
    
    def move(dx, dy):
        Mouse.moveInput.mi.dx = dx
        Mouse.moveInput.mi.dy = dy
        sendInput(1, byref(Mouse.moveInput), sizeof(Mouse.moveInput))
    move = staticmethod(move)
    
    def moveTo(x, y):
        Mouse.moveToInput.mi.dx = int((x - SCREENLEFT)*65536/SCREENWIDTH)
        Mouse.moveToInput.mi.dy = int((y - SCREENTOP)*65536/SCREENHEIGHT)
        sendInput(1, byref(Mouse.moveToInput), sizeof(Mouse.moveToInput))
    moveTo = staticmethod(moveTo)
    
    def press(button):
        Mouse.clickInput.mi.dwFlags = button;
        sendInput(1, byref(Mouse.clickInput), sizeof(Mouse.clickInput))
    press = staticmethod(press)
    
    def release(button):
        Mouse.clickInput.mi.dwFlags = button << 1;
        sendInput(1, byref(Mouse.clickInput), sizeof(Mouse.clickInput))
    release = staticmethod(release)
        
    def click(button):
        Mouse.press(button)
        Mouse.release(button)
    click = staticmethod(click)
    
    def scroll(scrollAmount):
        Mouse.scrollInput.mi.mouseData = int(scrollAmount * Mouse.WHEEL_DELTA);
        sendInput(1, byref(Mouse.scrollInput), sizeof(Mouse.scrollInput))
    scroll = staticmethod(scroll)
        
if __name__ == '__main__':
    Mouse.moveTo(50, SCREENHEIGHT - 50)
    Mouse.click(Mouse.LEFT)
    Mouse.move(10, -100)
