from ctypes import *
import win32api

user32 = windll.user32

# define SendInput function
sendInput = user32.SendInput

# get monitor info
for device in win32api.EnumDisplayMonitors():
    handle = device[0] # get device handle on monitor
    info = win32api.GetMonitorInfo(handle)
    if (info['Flags'] == 1): # if monitor is primary montor
        SCREENRECT = info['Monitor']
        (l, t, r, b) = SCREENRECT
        SCREENLEFT = l
        SCREENTOP = t
        SCREENRIGHT = r
        SCREENBOTTOM = b
        SCREENWIDTH = r - l
        SCREENHEIGHT = b - t
        SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT)
        break
