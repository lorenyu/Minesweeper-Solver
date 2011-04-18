from Gamepad import Gamepad
import events

Gamepad.AddEventController(events.ButtonEventController)
Gamepad.AddEventController(events.ButtonHeldEventController)
Gamepad.AddEventController(events.JoystickDirectionChangedEventController)
Gamepad.AddEventController(events.JoystickGestureEventController)

if __name__ == '__main__':
    print 'Press start on gameController to stop'

    g = Gamepad()
    events.ButtonHeldEvent.addTime(1)
    events.ButtonHeldEvent.addTime(2)

    def stopOnStart(gamepad, event):
        if event.buttonIndex == 9:
            gamepad.stop()
            
    g.addEventHandler(events.ButtonPressedEvent, stopOnStart)
    g.start()
    g.join()
