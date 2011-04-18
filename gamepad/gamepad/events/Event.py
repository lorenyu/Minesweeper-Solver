class Event:

    class Controller():
        
        def __init__(self, gamepad):
            self._gamepad = gamepad
            
        def poll(self):
            gamepad = self._gamepad
