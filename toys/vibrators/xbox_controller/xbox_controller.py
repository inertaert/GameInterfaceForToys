
from common.util import *
from toys.vibrators.vibrator import Vibrator



import ctypes
import time
import threading

# Define necessary structures
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

class XboxControllerInterface(Vibrator):
    def __init__(self):
        self.taskList = []
        t1 = threading.Thread(target=self.t1, args=(), daemon=True)
        t1.start()
        super().__init__("Xbox controller")
    
    def t1(self):
        # print('time thread '," running ....")
        xinput = ctypes.windll.xinput1_1
        XInputSetState = xinput.XInputSetState
        XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
        XInputSetState.restype = ctypes.c_uint
        self.taskList = []
        vibration = XINPUT_VIBRATION(int(1 * 65535), int(1 * 65535))
        XInputSetState(0, ctypes.byref(vibration))
        time.sleep(5)
        vibration = XINPUT_VIBRATION(int(0 * 65535), int(0 * 65535))
        XInputSetState(0, ctypes.byref(vibration))

        nowStrength = 0
        while True:
            time.sleep(0.5)
            r = 0
            newtaskList = []
            for i in self.taskList:
                i[0] -= 0.5
                if i[0] <= 0:
                    continue
                if i[1] > r:
                    r = i[1]
                newtaskList.append(i)
            self.taskList = newtaskList
            strength = r/100.0*0.8
            if strength > 0.01 : strength += 0.2
            if strength > 1: strength = 1
            # print("0.5s passed " + str(strength) + str(self.taskList))
            if nowStrength != strength:
                vibration = XINPUT_VIBRATION(int(strength * 65535), int(strength * 65535))
                XInputSetState(0, ctypes.byref(vibration))
                nowStrength = strength
    
    def shutdown(self):
        pass
        
    def connect(self):
        return

    def check_in(self):
        return
        

    def vibrate(self, duration, strength, pattern="", toys=[]):
        # print('addCommand',self.command)
        self.taskList.append([duration,strength])
    
    def stop(self):
        # print('cleanTaskList')
        self.taskList.clear()

    def shutdown(self):
        pass


    def get_toys(self):
        return {'Xbox Controller': {
            "name": "Xbox Controller",
            "interface": self.properties['name'],
            "id": "Xbox Controller",
            "battery": -1,
            "enabled": True
        }}


class XboxControllerInterfacePyGame(Vibrator):
    def __init__(self):
        import pygame
        pygame.init()

        self.controller_id = None

        # Try to find an Xbox controller, connect to the first one
        # fixme: Should probably accommodate multiple Xbox Controllers. Currently it just takes the first one.
        #  I'll devote time to this if users complain about it.
        for i in range(0, pygame.joystick.get_count()):
            if "Xbox" in pygame.joystick.Joystick(i).get_name():
                print(f"Detected controller: {pygame.joystick.Joystick(i).get_name()}, id={i}")
                self.controller_id = i
                break

        self.xbox_controller = pygame.joystick.Joystick(self.controller_id)

        self.taskList = []
        t1 = threading.Thread(target=self.t1, args=(), daemon=True)
        t1.start()
        super().__init__("Xbox controller")


    def t1(self):
        while True:
            time.sleep(0.5)

            if self.taskList:
                duration, strength = self.taskList.pop(0)  # FIFO
                print(f"XBOX PYGAME duration: {duration}")
                print(f"XBOX PYGAME strength: {strength}")
                strength = strength / 100  # Recast to 0.0-1.0 float
                duration = duration / 100  # fixme: Is duration supposed to be seconds, centi- or milliseconds?
                self.xbox_controller.rumble(strength, strength, 1000)  # Bug: duration argument does nothing.
                time.sleep(duration)
                self.xbox_controller.stop_rumble()


    def shutdown(self):
        pass

    def connect(self):
        return

    def check_in(self):
        return


    def vibrate(self, duration, strength, pattern="", toys=[]):
        # print('addCommand',self.command)
        self.taskList.append([duration, strength])


    def stop(self):
        # print('cleanTaskList')
        self.taskList.clear()

    def get_toys(self):
        return {'Xbox Controller': {
            "name": "Xbox Controller",
            "interface": self.properties['name'],
            "id": "Xbox Controller",
            "battery": -1,
            "enabled": True
        }}

