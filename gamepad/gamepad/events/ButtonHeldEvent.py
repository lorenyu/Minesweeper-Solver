from gamepad import Gamepad
from Event import Event
from ButtonEvent import ButtonPressedEvent, ButtonReleasedEvent

class ButtonHeldEvent(Event):

    _times = set()

    def addTime(time):
        ButtonHeldEvent._times.add(time)
    addTime = staticmethod(addTime)
    
    def removeTime(time):
        ButtonHeldEvent._times.remove(time)
    removeTime = staticmethod(removeTime)
    
    def getTimes():
        return list(ButtonHeldEvent._times)
    getTimes = staticmethod(getTimes)

    def __init__(self, buttonIndex, timeHeld):
        self.buttonIndex = buttonIndex
        self.timeHeld = timeHeld

    def __str__(self):
        return '<ButtonHeldEvent buttonIndex:%d timeHeld:%d>' % (self.buttonIndex, self.timeHeld)

class ButtonHeldEventController(Event.Controller):

    events = set([ButtonHeldEvent])

    def __init__(self, gamepad):
        self._time = gamepad.time
        self._timeIndices = [0]*gamepad.numButtons()
        self._buttonTimes = [0]*gamepad.numButtons()
        
        self._pressedButtons = set()
        
        gamepad.addEventHandler(ButtonPressedEvent, self._onButtonPressed)
        gamepad.addEventHandler(ButtonReleasedEvent, self._onButtonReleased)
        
    def poll(self, gamepad):
        times = ButtonHeldEvent.getTimes()
        buttonTimes = self._buttonTimes
        dt = gamepad.time - self._time
        
        for btn in self._pressedButtons:
            buttonTimes[btn] += dt
            i = self._timeIndices[btn]
            if i < len(times) and buttonTimes[btn] >= times[i]:
                gamepad.fireEvent(ButtonHeldEvent(btn, times[i]))
                self._timeIndices[btn] += 1
        
        self._time = gamepad.time

    def _onButtonPressed(self, gamepad, event):
        self._pressedButtons.add(event.buttonIndex)
        
    def _onButtonReleased(self, gamepad, event):
        i = event.buttonIndex
        self._pressedButtons.remove(i)
        self._buttonTimes[i] = 0
        self._timeIndices[i] = 0
