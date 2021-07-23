import logging
import time
import RPi.GPIO as GPIO


class RelayController():
    """Class for controlling the relay"""

    def __init__(self):
        self._set_defaults()
        self._setup_gpio()
        print('Testing system')
        self.activate_solenoid()

    def __del__(self):
        GPIO.cleanup()

    def _set_defaults(self):
        """Set defaults for the application"""
        self.air_solenoid_running_timeout_seconds = 2
        self.air_solenoid_pin_bcm = 22

    def _setup_gpio(self):
        """Set up the GPIO defaults"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.air_solenoid_pin_bcm, GPIO.OUT)
        GPIO.output(self.air_solenoid_pin_bcm, 1)

    def _cycle_pin(self, pin, timeout):
        GPIO.output(pin, 0)
        time.sleep(timeout)
        GPIO.output(pin, 1)

    def activate_solenoid(self):
        """Activates the air solenoid."""
        logging.info('Activating air solenoid')
        self._cycle_pin(self.air_solenoid_pin_bcm, self.air_solenoid_running_timeout_seconds)
        logging.info('Deactivating air solenoid')
