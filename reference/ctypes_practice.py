from ctypes import *

class DeviceInput(Union):
    _fields_ = [('mi', c_int),
                ('ki', c_int),
                ('hi', c_int)]

class INPUT(Structure):
    _fields_ = [('type', c_int),
                ("i", DeviceInput)]
    _anonymous_ = ("i")

print INPUT.type
print INPUT.mi
print INPUT.ki
print INPUT.hi