from .chain import chainFK


class Finger(chainFK.ChainFK):

    def __init__(
            self,
            side,
            name='finger',
            segment=4,
            length=2.0):

        direction = [-1, 0, 0]
        if side == 'L':
            direction = [1, 0, 0]

        chainFK.ChainFK.__init__(self, side, name, segment, length, direction)
