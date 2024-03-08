from interfaces.interface import Interface


class PixelReaderInterface(Interface):
    def __init__(self, toy_type):
        Interface.__init__(self, "Pixel reader", toy_type)

    def execute(self):
        pass
