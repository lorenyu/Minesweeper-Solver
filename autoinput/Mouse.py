from ctypes import *
from structs import *
from interop import *

class Mouse():

    # constants

    class MouseEvent:
        MOVE = 0x0001;
        LEFTDOWN = 0x0002;
        LEFTUP = 0x0004;
        RIGHTDOWN = 0x0008;
        RIGHTUP = 0x0010;
        MIDDLEDOWN = 0x0020;
        MIDDLEUP = 0x0040;
        XDOWN = 0x0080;
        XUP = 0x0100;
        WHEEL = 0x0800;
        VIRTUALDESK = 0x4000;
        ABSOLUTE = 0x8000;
        
    XBUTTON1 = 0x0001;
    XBUTTON2 = 0x0002;
    WHEEL_DELTA = 120;
    
    LEFT = MouseEvent.LEFTDOWN
    RIGHT = MouseEvent.RIGHTDOWN
    MIDDLE = MouseEvent.MIDDLEDOWN
    NUMBUTTONS = 3

    # structures to pass to SendInput (preinitialized for efficiency)
    
    _moveInput = INPUT()
    _moveInput.type = INPUT.MOUSE
    _moveInput.mi.dwFlags = MouseEvent.MOVE
    _moveInput.mi.dwExtraInfo = 0
    _moveInput.mi.mouseData = 0
    _moveInput.mi.time = 0
    
    _moveToInput = INPUT()
    _moveToInput.type = INPUT.MOUSE
    _moveToInput.mi.dwFlags = MouseEvent.ABSOLUTE + MouseEvent.MOVE
    _moveToInput.mi.dwExtraInfo = 0
    _moveToInput.mi.mouseData = 0
    _moveToInput.mi.time = 0
    
    _clickInput = INPUT()
    _clickInput.type = INPUT.MOUSE;
    _clickInput.mi.dwExtraInfo = 0;
    _clickInput.mi.mouseData = 0;
    _clickInput.mi.time = 0;
    
    _scrollInput = INPUT()
    _scrollInput.type = INPUT.MOUSE;
    _scrollInput.mi.dwFlags = MouseEvent.WHEEL;
    _scrollInput.mi.dwExtraInfo = 0;
    _scrollInput.mi.time = 0;
    
    def move(dx, dy):
        Mouse._moveInput.mi.dx = dx
        Mouse._moveInput.mi.dy = dy
        sendInput(1, byref(Mouse._moveInput), sizeof(Mouse._moveInput))
    move = staticmethod(move)
    
    def moveTo(x, y):
        Mouse._moveToInput.mi.dx = int((x - SCREENLEFT)*65536/SCREENWIDTH)
        Mouse._moveToInput.mi.dy = int((y - SCREENTOP)*65536/SCREENHEIGHT)
        sendInput(1, byref(Mouse._moveToInput), sizeof(Mouse._moveToInput))
    moveTo = staticmethod(moveTo)
    
    def press(button):
        Mouse._clickInput.mi.dwFlags = button;
        sendInput(1, byref(Mouse._clickInput), sizeof(Mouse._clickInput))
    press = staticmethod(press)
    
    def release(button):
        Mouse._clickInput.mi.dwFlags = button << 1;
        sendInput(1, byref(Mouse._clickInput), sizeof(Mouse._clickInput))
    release = staticmethod(release)
        
    def click(button):
        Mouse.press(button)
        Mouse.release(button)
    click = staticmethod(click)
    
    def scroll(scrollAmount):
        Mouse._scrollInput.mi.mouseData = int(scrollAmount * Mouse.WHEEL_DELTA);
        sendInput(1, byref(Mouse._scrollInput), sizeof(Mouse._scrollInput))
    scroll = staticmethod(scroll)
        
if __name__ == '__main__':
    Mouse.moveTo(50, SCREENHEIGHT - 50)
    Mouse.click(Mouse.LEFT)
    Mouse.move(10, -100)
