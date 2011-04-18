from ctypes import *
from structs import *
from interop import *

class Keyboard():

    # constants

    class KeyEvent:
        EXTENDEDKEY = 0x0001
        KEYUP = 0x0002
        UNICODE = 0x0004
        SCANCODE = 0x0008    

    class VirtualKeys:
        LBUTTON = 0x01
        RBUTTON = 0x02
        CANCEL = 0x03
        MBUTTON = 0x04    # NOT contiguous with L & RBUTTON

        BACK = 0x08
        TAB = 0x09

        CLEAR = 0x0C
        RETURN = 0x0D

        SHIFT = 0x10
        CONTROL = 0x11
        MENU = 0x12
        PAUSE = 0x13
        CAPITAL = 0x14

        ESCAPE = 0x1B

        SPACE = 0x20
        PRIOR = 0x21
        NEXT = 0x22
        END = 0x23
        HOME = 0x24
        LEFT = 0x25
        UP = 0x26
        RIGHT = 0x27
        DOWN = 0x28
        SELECT = 0x29
        PRINT = 0x2A
        EXECUTE = 0x2B
        SNAPSHOT = 0x2C
        INSERT = 0x2D
        DELETE = 0x2E
        HELP = 0x2F

        # 0 thru 9 are the same as ASCII '0' thru '9' (= 0x30 - = 0x39)
        # A thru Z are the same as ASCII 'A' thru 'Z' (= 0x41 - = 0x5A)

        LWIN = 0x5B
        RWIN = 0x5C
        APPS = 0x5D

        NUMPAD0 = 0x60
        NUMPAD1 = 0x61
        NUMPAD2 = 0x62
        NUMPAD3 = 0x63
        NUMPAD4 = 0x64
        NUMPAD5 = 0x65
        NUMPAD6 = 0x66
        NUMPAD7 = 0x67
        NUMPAD8 = 0x68
        NUMPAD9 = 0x69
        MULTIPLY = 0x6A
        ADD = 0x6B
        SEPARATOR = 0x6C
        SUBTRACT = 0x6D
        DECIMAL = 0x6E
        DIVIDE = 0x6F
        F1 = 0x70
        F2 = 0x71
        F3 = 0x72
        F4 = 0x73
        F5 = 0x74
        F6 = 0x75
        F7 = 0x76
        F8 = 0x77
        F9 = 0x78
        F10 = 0x79
        F11 = 0x7A
        F12 = 0x7B
        F13 = 0x7C
        F14 = 0x7D
        F15 = 0x7E
        F16 = 0x7F
        F17 = 0x80
        F18 = 0x81
        F19 = 0x82
        F20 = 0x83
        F21 = 0x84
        F22 = 0x85
        F23 = 0x86
        F24 = 0x87

        NUMLOCK = 0x90
        SCROLL = 0x91

        # L* & R* - left and right Alt Ctrl and Shift virtual keys.
        # Used only as parameters to GetAsyncKeyState() and GetKeyState().
        # No other API or message will distinguish left and right keys in this way.
        LSHIFT = 0xA0
        RSHIFT = 0xA1
        LCONTROL = 0xA2
        RCONTROL = 0xA3
        LMENU = 0xA4
        RMENU = 0xA5

        PROCESSKEY = 0xE5

        ATTN = 0xF6
        CRSEL = 0xF7
        EXSEL = 0xF8
        EREOF = 0xF9
        PLAY = 0xFA
        ZOOM = 0xFB
        NONAME = 0xFC
        PA1 = 0xFD
        OEM_CLEAR = 0xFE

    for i in range(0, 10):
        setattr(VirtualKeys, 'NUM' + str(i), ord(str(i)))

    for i in range(ord('A'), ord('Z')+1):
        setattr(VirtualKeys, chr(i), ord(chr(i)))

    class PhysicalKeys:
        Tilde =     0x29
        Key_1 =     0x2
        Key_2 =     0x3
        Key_3 =     0x4
        Key_4 =     0x5
        Key_5 =     0x6
        Key_6 =     0x7
        Key_7 =     0x8
        Key_8 =     0x9
        Key_9 =     0x0A
        Key_0 =     0x0B
        Dash =     0x0C
        Equals =     0x0D
        Backspace =     0x0E
        Tab =     0x0F
        Q =     0x10
        W =     0x11
        E =     0x12
        R =     0x13
        T =     0x14
        Y =     0x15
        U =     0x16
        I =     0x17
        O =     0x18
        P =     0x19
        LeftSquareBracket =     0x1A
        RightSquareBracket =     0x1B
        Backslash =     0x2B
        CapsLock =     0x3A
        A =     0x1E
        S =     0x1F
        D =     0x20
        F =     0x21
        G =     0x22
        H =     0x23
        J =     0x24
        K =     0x25
        L =     0x26
        Semicolon =     0x27
        Apostrophe =     0x28
        Enter =     0x1C
        LeftShift =     0x2A
        Z =     0x2C
        X =     0x2D
        C =     0x2E
        V =     0x2F
        B =     0x30
        N =     0x31
        M =     0x32
        Comma =     0x33
        Period =     0x34
        ForwardSlash =     0x35
        RightShift =     0x36
        LeftControl =     0x1D
        LeftAlt =     0x38
        SpaceBar =     0x39
        RightAlt =     0xE038
        RightControl =     0xE01D
                
        Insert =     0xE052
        Delete =     0xE053
        LeftArrow =     0xE04B
        Home =     0xE047
        End =     0xE04F
        UpArrow =     0xE048
        DnArrow =     0xE050
        PageUp =     0xE049
        PageDown =     0xE051
        RightArrow =     0xE04D

        NumLock =     0x45
        Numeric7 =     0x47
        Numeric4 =     0x4B
        Numeric1 =     0x4F
        #NumericDivide =     Note 3
        Numeric8 =     0x48
        Numeric5 =     0x4C
        Numeric2 =     0x50
        Numeric0 =     0x52
        NumericTimes =     0x37
        Numeric9 =     0x49
        Numeric6 =     0x4D
        Numeric3 =     0x51
        NumericDecimal =     0x53
        NumericMinus =     0x4A
        NumericPlus =     0x4E
        NumericEnter =     0xE01C
        Esc =     1
        F1 =     0x3B
        F2 =     0x3C
        F3 =     0x3D
        F4 =     0x3E
        F5 =     0x3F
        F6 =     0x40
        F7 =     0x41
        F8 =     0x42
        F9 =     0x43
        F10 =     0x44
        F11 =     0x57
        F12 =     0x58
        ScrollLock =     0x46
        LeftWin =     0x5C
        RightWin =     0x5D
        Application =     0x5E

    # structures to pass to SendInput (preinitialized for efficiency)

    _virtualKeyInput = INPUT()
    _virtualKeyInput.type = INPUT.KEYBOARD
    _virtualKeyInput.ki.dwExtraInfo = 0
    _virtualKeyInput.ki.wScan = 0
    _virtualKeyInput.ki.time = 0

    _physicalKeyInput = INPUT()
    _physicalKeyInput.type = INPUT.KEYBOARD
    _physicalKeyInput.ki.dwExtraInfo = 0
    _physicalKeyInput.ki.time = 0
    
    def press(keyCode, virtual=True):
        '''Simulate pressing of virtual key (default) or physical key.'''
        if virtual:
            Keyboard._virtualKeyInput.ki.wVk = keyCode

            Keyboard._virtualKeyInput.ki.dwFlags = 0
            sendInput(1, byref(Keyboard._virtualKeyInput), sizeof(Keyboard._virtualKeyInput))
        else:
            Keyboard._physicalKeyInput.ki.wScan = keyCode

            Keyboard._physicalKeyInput.ki.dwFlags = Keyboard.KeyEvent.SCANCODE
            sendInput(1, byref(Keyboard._physicalKeyInput), sizeof(Keyboard._physicalKeyInput))
    press = staticmethod(press)
    
    def release(keyCode, virtual=True):
        if virtual:
            Keyboard._virtualKeyInput.ki.wVk = keyCode

            Keyboard._virtualKeyInput.ki.dwFlags = Keyboard.KeyEvent.KEYUP
            sendInput(1, byref(Keyboard._virtualKeyInput), sizeof(Keyboard._virtualKeyInput))
        else:
            Keyboard._physicalKeyInput.ki.wScan = keyCode

            Keyboard._physicalKeyInput.ki.dwFlags = Keyboard.KeyEvent.SCANCODE | Keyboard.KeyEvent.KEYUP
            sendInput(1, byref(Keyboard._physicalKeyInput), sizeof(Keyboard._physicalKeyInput))
    release = staticmethod(release)
        
if __name__ == '__main__':
    from Mouse import Mouse
    Mouse.moveTo(50, SCREENHEIGHT - 50)
    Mouse.click(Mouse.LEFT)
    Keyboard.press(Keyboard.VirtualKeys.R)
    Keyboard.release(Keyboard.VirtualKeys.R)
    Keyboard.press(Keyboard.VirtualKeys.R)
    Keyboard.release(Keyboard.VirtualKeys.R)
