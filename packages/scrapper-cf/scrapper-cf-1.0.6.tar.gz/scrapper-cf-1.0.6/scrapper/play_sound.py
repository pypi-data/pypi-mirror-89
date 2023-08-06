import os
import platform
import time

# This plays a beep sound based on OS
def play_beep():
    '''
    This plays a beep sound based on OS
    '''
    os_name = platform.system()

    if (os_name == 'Linux' or os_name == 'Mac'):
        duration = 1  # seconds
        freq = 440  # Hz
        for i in range(0,3): # How many beeps. We can make this configurable later.
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
            time.sleep(1)
    elif(os_name == 'Windows'):
        import winsound
        duration = 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)