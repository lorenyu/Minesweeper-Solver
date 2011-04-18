from gamepad import Gamepad
from Event import Event

class ButtonEvent(Event):

    def __init__(self, buttonIndex, pressed):
        self.buttonIndex = buttonIndex
        self.pressed = pressed
        
    def __str__(self):
        if self.pressed:
            text = 'pressed'
        else:
            text = 'released'
        return '<ButtonEvent %s buttonIndex:%d>' % (text, self.buttonIndex)

class ButtonPressedEvent(ButtonEvent):

    def __init__(self, buttonIndex):
        ButtonEvent.__init__(self, buttonIndex, True)
        
    def __str__(self):
        return '<ButtonPressedEvent buttonIndex:%d>' % self.buttonIndex

class ButtonReleasedEvent(ButtonEvent):

    def __init__(self, buttonIndex):
        ButtonEvent.__init__(self, buttonIndex, False)

    def __str__(self):
        return '<ButtonReleasedEvent buttonIndex:%d>' % self.buttonIndex

class ButtonEventController(Event.Controller):

    events = set([ButtonPressedEvent, ButtonReleasedEvent])

    def __init__(self, gamepad):
        self._buttonStates = [False]*gamepad.numButtons()
        
    def poll(self, gamepad):
        buttonStates = self._buttonStates
        
        for i in range(0, gamepad.numButtons()):
            buttonState = gamepad.buttonState(i)
            if buttonState != buttonStates[i]:
                if buttonState:
                    gamepad.fireEvent(ButtonPressedEvent(i))
                else:
                    gamepad.fireEvent(ButtonReleasedEvent(i))
            buttonStates[i] = buttonState
