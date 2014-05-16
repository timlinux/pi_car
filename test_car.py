"""Simple little python script to control a little toy car.

This code requires a piface board to be setup and the python digitalio libs
installed.

sudo apt-get install python{,3}-pifacedigitalio

Add this to your /etc/rc.local:

/usr/bin/python -u /home/pi/pi_car/test_car.py
"""

import time
import pifacedigitalio

LED_PIN = 7


def wait(period):
    """Wait for a while.

    :param period: Time in ms to wait for.
    :param period: int
    """
    period /= 1000
    target_time = time.clock() + period
    while time.clock() < target_time:
        pass


def restart():
    """Restart the computer (useful if you have updated this script).

    ..note:: This script must have been run by root for this function to work.

    """
    print 'Restarting'
    command = '/usr/bin/sudo /sbin/shutdown -r now'
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def halt():
    """Halt the computer (useful if you have updated this script).

    ..note:: This script must have been run by root for this function to work.

    """
    print 'Shutting down'
    command = '/usr/bin/sudo /sbin/shutdown now'
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def flash_led(count, duration):
    """Flash the led.

    :param count: Number of times to flash.
    :param duration: Length of time in ms for each flash.
    """
    for value in xrange(0, 10):
        pifacedigital.leds[LED_PIN].turn_on()
        wait(1500)
        pifacedigital.leds[LED_PIN].turn_off()
        wait(1500)


def switch_pressed(event):
    """When user presses wait a second then let the motor start.

    If it is button 0 (forward) or button 1 (backward) the led on pin 7 will
    be turned on.

    """
    if event.pin_num == 2:  # reboot
        # Short flash the led to show we are restarting
        flash_led(5, 500)
        restart()

    elif event.pin_num == 3: # halt
        # Long flash the led to show we are shutting down
        flash_led(10, 1500)
        halt()

    elif event.pin_num in [0, 1]:
        # Go forwards (0) or backwards (1)
        event.chip.output_pins[event.pin_num].turn_on()
        # Turn on the led on pin 7 too
        pifacedigital.leds[LED_PIN].turn_on()


def switch_unpressed(event):
    """When user releases let the motor run for 25 ms then stop it."""
    wait(250)
    event.chip.output_pins[event.pin_num].turn_off()
    # Turn off the led on pin 7 after waiting an extra second
    wait(250)
    pifacedigital.leds[LED_PIN].turn_off()


if __name__ == "__main__":
    pifacedigital = pifacedigitalio.PiFaceDigital()

    # Flash the led to show we are online
    flash_led(10, 500)

    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)
    listener.activate()
