from gamepad import Gamepad
from Event import Event
from EventSequenceMachine import SequenceAutomata
from JoystickDirection import JoystickDirection
from JoystickDirectionChangedEvent import JoystickDirectionChangedEvent

class Gesture:

    def __init__(self, name, directionSequence, maxGestureTime = 0.75):
        self.name = name
        self.directionSequence = directionSequence
        self.maxGestureTime = maxGestureTime
    
class JoystickGestureEvent(Event):

    gestures = []
    
    def addGesture(name, directionSequence, maxGestureTime = 0.50):
        gesture = Gesture(name, directionSequence, maxGestureTime)
        JoystickGestureEvent.gestures.append(gesture)
    addGesture = staticmethod(addGesture)

    def __init__(self, joystickIndex, name, gestureTime):
        '''name needs to be unique'''
        self.name = name
        self.gestureTime = gestureTime

    def __str__(self):
        return '<JoystickGestureEvent name:%s gestureTime:%.2fs>' % (self.name, self.gestureTime)

class JoystickGestureEventController(Event.Controller):

    events = set([JoystickGestureEvent])
    
    def __init__(self, gamepad):
        self._automata = {}
        self._gestureTimes = {}
        for gesture in JoystickGestureEvent.gestures:
            self.addGesture(gesture)
            
        gamepad.addEventHandler(JoystickDirectionChangedEvent, self._onDirectionChanged)
        
    def addGesture(self, gesture):
        (name, directionSequence, maxGestureTime) = (gesture.name, gesture.directionSequence, gesture.maxGestureTime)
        automaton = SequenceAutomata(directionSequence, JoystickDirection.AllDirections)
        self._automata[name] = automaton
        self._gestureTimes[name] = [0]*len(directionSequence)
        
    def poll(self, gamepad):
        pass
        
    def _onDirectionChanged(self, gamepad, directionChangedEvent):
        gestures = JoystickGestureEvent.gestures
        automata = self._automata
        gestureTimes = self._gestureTimes
        joystickIndex = directionChangedEvent.joystickIndex
        direction = directionChangedEvent.direction
        
        for i in range(0, len(gestures)):
            (name, maxGestureTime) = (gestures[i].name, gestures[i].maxGestureTime)
        
            if not automata.has_key(name):
                self.addGesture(gestures[i])
            
            automaton = automata[name]
                
            times = gestureTimes[name]
            times.pop(0)
            times.append(gamepad.time)

            if direction != None:
                automaton.transition(direction)
                
                if automaton.accept():
                    gestureTime = times[len(times) - 1] - times[0]
                    if gestureTime <= maxGestureTime:
                        gamepad.fireEvent(JoystickGestureEvent(joystickIndex, name, gestureTime))
                        automaton.reset()
