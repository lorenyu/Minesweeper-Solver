class Direction:
    Center    = 0
    Up        = 1 << 0
    Left      = 1 << 1
    Down      = 1 << 2
    Right     = 1 << 3
    UpLeft    = Up + Left
    UpRight   = Up + Right
    DownLeft  = Down + Left
    DownRight = Down + Right
    AllDirections = set([Center, Up, Left, Down, Right, UpLeft, UpRight, DownLeft, DownRight])
    
    _strings = ['Invalid direction']*(max(AllDirections) + 1)
    _strings[Center]    = 'Center'
    _strings[Up]        = 'Up'
    _strings[Left]      = 'Left'
    _strings[Down]      = 'Down'
    _strings[Right]     = 'Right'
    _strings[UpLeft]    = 'UpLeft'
    _strings[UpRight]   = 'UpRight'
    _strings[DownLeft]  = 'DownLeft'
    _strings[DownRight] = 'DownRight'
        
    def str(direction):
        return Direction._strings[direction]
    str = staticmethod(str)
    
class JoystickDirection(Direction):

    _map = {( 0, 0) : Direction.Center,
        ( 0,-1) : Direction.Up,
        (-1, 0) : Direction.Left,
        ( 0, 1) : Direction.Down,
        ( 1, 0) : Direction.Right,
        (-1,-1) : Direction.UpLeft,
        ( 1,-1) : Direction.UpRight,
        (-1, 1) : Direction.DownLeft,
        ( 1, 1) : Direction.DownRight}

    def direction(joystickPositionSquare):
        if not JoystickDirection._map.has_key(joystickPositionSquare):
            return None
        return JoystickDirection._map[joystickPositionSquare]
    direction = staticmethod(direction)