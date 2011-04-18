from ctypes import *

# The field 'dwExtraInfo' isn't properly defined in any of these structs
class MOUSEINPUT(Structure):
    _fields_ = [('dx', c_int),
                ('dy', c_int),
                ('mouseData', c_uint),
                ('dwFlags', c_uint),
                ('time', c_uint),
                ('dwExtraInfo', c_uint)]

class KEYBDINPUT(Structure):
    _fields_ = [('wVk', c_ushort),
                ('wScan', c_uint),
                ('dwFlags', c_uint),
                ('time', c_uint),
                ('dwExtraInfo', c_uint)]

class HARDWAREINPUT(Structure):
    _fields_ = [('uMsg', c_uint),
                ('wParamL', c_ushort),
                ('wParamH', c_ushort)]

class DEVICEINPUT(Union):
    _fields_ = [('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT)]

class INPUT(Structure):
    _fields_ = [('type', c_int),
                ('i', DEVICEINPUT)]
    _anonymous_ = ('i')
    
    MOUSE = 0
    KEYBOARD = 1
    HARDWARE = 2

if __name__ == '__main__':
    print 'struct INPUT: (size=', sizeof(INPUT), ')'
    for field in dir(INPUT):
        if not str(field).startswith('_'):
            print '\t', str(field), '\t', getattr(INPUT, str(field))
    print
            
    print 'struct MOUSEINPUT: (size=', sizeof(MOUSEINPUT), ')'
    for field in dir(MOUSEINPUT):
        if not str(field).startswith('_'):
            print '\t', str(field), '\t', getattr(MOUSEINPUT, str(field))
    print
            
    print 'struct KEYBDINPUT: (size=', sizeof(KEYBDINPUT), ')'
    for field in dir(KEYBDINPUT):
        if not str(field).startswith('_'):
            print '\t', str(field), '\t', getattr(KEYBDINPUT, str(field))
    print
            
    print 'struct HARDWAREINPUT: (size=', sizeof(HARDWAREINPUT), ')'
    for field in dir(HARDWAREINPUT):
        if not str(field).startswith('_'):
            print '\t', str(field), '\t', getattr(HARDWAREINPUT, str(field))
    print