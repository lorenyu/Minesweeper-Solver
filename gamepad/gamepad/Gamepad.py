import clr
from time import time

# modify PYTHONPATH to include the directory containing Microsoft.DirectX.DirectInput.dll so clr module can find it
import sys
sys.path.append('C:\\WINDOWS\\Microsoft.NET\\DirectX for Managed Code\\1.0.2902.0\\')

# Add the reference to the DirectInput dll.
# Then import the objects defined in the dll, such as
# Microsoft.DirectX.DirectInput.Manager, DeviceClass, EnumDevicesFlags, DeviceList, etc.
clr.AddReference("Microsoft.DirectX.DirectInput")
from Microsoft.DirectX.DirectInput import *

import math
maxshort = (1 << 15) - 1
maxushort = (1 << 16) - 1
from threading import Thread

class Gamepad(Thread):

    #### Static variables ####

    NumButtons = 12 # TODO: is there any way to figure this out dynamically?
    
    class JoystickCoordinateTypes:
        Raw        = 0
        UnitCircle = 1
        UnitSquare = 2
    
    _gamepads = []
    _eventControllers = set()
    events = set()

    def _get_gamepads():
        '''Returns list of joystick devices currently connected to the computer.'''
        gamepads = []
        deviceList = Manager.GetDevices(DeviceClass.All, EnumDevicesFlags.AllDevices)
        for device in deviceList:
            print device
            if (device.DeviceType in [DeviceType.Joystick, DeviceType.Gamepad]):
                gamepads.append(device)
        return gamepads
    _gamepads = _get_gamepads()

    #### Static methods ####

    def NumGamepads(cls):
        '''Returns number of joystick devices currently connected to the computer.'''
        return len(Gamepad._gamepads)
    NumGamepads = classmethod(NumGamepads)
    
    def AddEventController(eventControllerClass):
        Gamepad._eventControllers.add(eventControllerClass)
        Gamepad.events.update(eventControllerClass.events)
    AddEventController = staticmethod(AddEventController)

    #### Instance methods ####
    
    def __init__(self, gamepadIndex = 0):
        '''gamepadIndex is an integer >= 0 and < NumGamepads()'''

        Thread.__init__(self)

        if self.NumGamepads() <= 0:
            raise Exception, 'There are no gamepads connected to computer'
        
        if gamepadIndex < 0 or gamepadIndex >= self.NumGamepads():
            raise Exception, 'gamepadIndex must be an integer from 0 to NumGamepads() - 1'
        
        device = Device(self._gamepads[gamepadIndex].InstanceGuid)
        device.Acquire()

        self.debug = False
        self.gamepadIndex = gamepadIndex
        self._device = device
        
        self.running = False
        self.time = time()
        
        (self._leftX, self._leftY) = (None, None)
        (self._rightX, self._rightY) = (None, None)
        self._buttonStates = None
        
        self.gamepadCallbacks = []
        self.eventHandlers= {}
        
        # Add event controllers' poll callbacks to the main loop (self.gamepadCallbacks and self.eventHandlers must be defined by this point)
        
        for eventController in Gamepad._eventControllers:
            self.addGamepadCallback(eventController(self).poll)
        

    def __del__(self):
        '''destructor releases gamepad'''
        self._device.Unacquire()

    def run(self):
        '''Start main loop.'''
        self.running = True
        while self.running:
            self.poll()

    def stop(self):
        '''Stop main loop.'''
        self.running = False

    def addGamepadCallback(self, callback):
        '''Runs a handler every iteration of the main loop after updating the gamepad device state.'''
        self.gamepadCallbacks.append(callback)
        
    def addEventHandler(self, eventClass, callback):
        handlers = self.eventHandlers

        if not handlers.has_key(eventClass):
            handlers[eventClass] = []
        handlers[eventClass].append(callback)

    def fireEvent(self, event):
        if self.debug == True:
            print event
        eventClass = event.__class__

        if not self.eventHandlers.has_key(eventClass):
            return
        
        for callback in self.eventHandlers[eventClass]:
            callback(self, event)

    def poll(self):
        self.update()

        for callback in self.gamepadCallbacks:
            callback(self)

    def update(self):
        device = self._device
        
        device.Poll()
        self.time = time()
        self._leftX = max(device.CurrentJoystickState.X - maxshort - 1, -maxshort)
        self._leftY = max(device.CurrentJoystickState.Y - maxshort - 1, -maxshort)
        self._rightX = max(device.CurrentJoystickState.Rz - maxshort - 1, -maxshort)
        self._rightY = max(device.CurrentJoystickState.Z - maxshort - 1, -maxshort)
        self._buttonStates = device.CurrentJoystickState.GetButtons()

    def leftJoystickPosition(self, coordType = JoystickCoordinateTypes.UnitCircle):
        if coordType == Gamepad.JoystickCoordinateTypes.UnitCircle:
            return self._joystickPosition(self._leftX, self._leftY)
        elif coordType == Gamepad.JoystickCoordinateTypes.UnitSquare:
            return self._joystickPositionSquare(self._leftX, self._leftY)
        else:
            return (self._leftX, self._leftY)

    def leftJoystickMagnitude(self):
        return self._joystickMagnitude(self._leftX, self._leftY)

    def rightJoystickPosition(self, coordType = JoystickCoordinateTypes.UnitCircle):
        if coordType == Gamepad.JoystickCoordinateTypes.UnitCircle:
            return self._joystickPosition(self._rightX, self._rightY)
        elif coordType == Gamepad.JoystickCoordinateTypes.UnitSquare:
            return self._joystickPositionSquare(self._rightX, self._rightY)
        else:
            return (self._rightX, self._rightY)

    def rightJoystickMagnitude(self):
        return self._joystickMagnitude(self._rightX, self._rightY)

    def numButtons(self):
        return Gamepad.NumButtons

    def buttonState(self, buttonIndex):
        if buttonIndex < 0 or buttonIndex >= self.numButtons():
            raise Exception, 'buttonIndex out of bounds.'
        
        if self._buttonStates[buttonIndex] != 0:
            return True
        else:
            return False

    def _joystickPosition(self, joystickX, joystickY):
        (x, y) = (0, 0)
        if (joystickX != 0 or joystickY != 0):
            l = math.sqrt(joystickX**2 + joystickY**2)
            magnitude = self._joystickMagnitude(joystickX, joystickY)
        if (joystickX != 0):
            x = magnitude * joystickX / l
        if (joystickY != 0):
            y = magnitude * joystickY / l
        return (x, y)
        
    def _joystickPositionSquare(self, joystickX, joystickY):
        return (joystickX / maxshort, joystickY / maxshort)

    def _joystickMagnitude(self, joystickX, joystickY):
        return float(max(abs(joystickX), abs(joystickY))) / maxshort

if __name__ == '__main__':
    
    print 'Press L1, L2, R1, and R2 on gameController all at same time to stop'
    
    g = Gamepad()
    
    def joystick(gamepad):
        ((leftX, leftY), (rightX, rightY)) = (g.leftJoystickPosition(Gamepad.JoystickCoordinateTypes.UnitSquare), g.rightJoystickPosition(Gamepad.JoystickCoordinateTypes.UnitSquare))
        if abs(leftX) == 1 or abs(leftY) == 1 or abs(rightX) == 1 or abs(rightY) == 1:
            print (leftX, leftY), (rightX, rightY)
    g.addGamepadCallback(joystick)

    def stop(gamepad):
        shouldStop = True
        for btn in [4,5,6,7]:
            shouldStop &= gamepad.buttonState(btn)
        if shouldStop:
            gamepad.stop()
    g.addGamepadCallback(stop)
    
    g.start()
    g.join()

