from gamepad import Gamepad
from Event import Event
from ButtonEvent import ButtonPressedEvent, ButtonReleasedEvent
from JoystickDirection import JoystickDirection

class JoystickDirectionChangedEvent(Event):

    joysticks = ['leftJoystick', 'rightJoystick']

    def __init__(self, joystickIndex, direction, oldDirection):
        self.joystickIndex = joystickIndex
        self.direction = direction
        self.oldDirection = oldDirection

    def __str__(self):
        joystick = JoystickDirectionChangedEvent.joysticks[self.joystickIndex]
        return '<JoystickDirectionChangedEvent ' + joystick + ' direction:%s oldDirection:%s>' % (JoystickDirection.str(self.direction), JoystickDirection.str(self.oldDirection))

class JoystickDirectionChangedEventController(Event.Controller):

    events = set([JoystickDirectionChangedEvent])

    def __init__(self, gamepad):
        self._leftJoystickDirection = JoystickDirection.Center
        self._rightJoystickDirection = JoystickDirection.Center
        
    def poll(self, gamepad):
        
        leftPos = gamepad.leftJoystickPosition(Gamepad.JoystickCoordinateTypes.UnitSquare)
        rightPos = gamepad.rightJoystickPosition(Gamepad.JoystickCoordinateTypes.UnitSquare)
        
        leftJoystickDirection = JoystickDirection.direction(leftPos)
        rightJoystickDirection = JoystickDirection.direction(rightPos)
        
        if leftJoystickDirection != self._leftJoystickDirection:
            gamepad.fireEvent(JoystickDirectionChangedEvent(0, leftJoystickDirection, self._leftJoystickDirection))
        
        if rightJoystickDirection != self._rightJoystickDirection:
            gamepad.fireEvent(JoystickDirectionChangedEvent(1, rightJoystickDirection, self._rightJoystickDirection))
            
        self._leftJoystickDirection = leftJoystickDirection
        self._rightJoystickDirection = rightJoystickDirection
