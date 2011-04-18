# test.py

from gamepad import *
from gamepad.events import *

if __name__ == '__main__':
    print 'Press start on gameController to stop'

    g = Gamepad()
    ButtonHeldEvent.addTime(1)
    ButtonHeldEvent.addTime(2)
    
    u,l,d,r = JoystickDirection.Up, JoystickDirection.Left, JoystickDirection.Down, JoystickDirection.Right
    
    JoystickGestureEvent.addGesture('DownRollRight', [d,d+r,r])
    JoystickGestureEvent.addGesture('DownRollLeft', [d,d+l,l])
    JoystickGestureEvent.addGesture('LeftRollDown', [l,l+d,d])
    JoystickGestureEvent.addGesture('RightRollDown', [r,r+d,d])
    JoystickGestureEvent.addGesture('LeftRollRight', [l,l+d,d,d+r,r])
    JoystickGestureEvent.addGesture('DownClockwise360', [d,d+r,r,r+u,u,u+l,l,l+d,d])
    JoystickGestureEvent.addGesture('DownCounterclockwise360', [d,d+l,l,l+u,u,u+r,r,r+d,d])

    def stopOnStart(gamepad, event):
        if event.buttonIndex == 9:
            gamepad.stop()
            
    g.addEventHandler(ButtonPressedEvent, stopOnStart)
    g.start()
    g.join()