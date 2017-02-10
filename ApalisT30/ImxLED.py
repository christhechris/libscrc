# -*- coding:utf8 -*-
""" Apalis T30 LED."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: i.mx6 ARMv7
# Author:   Heyn
# Program:  ImxLED.
# History:  2017/02/09

import pwm

class ImxLED:
    """Apalis T30 ImxPWM Class."""

    def __init__(self, channel='LED1'):
        super(ImxLED, self).__init__()

        self.status = True
        dic = {'LED1' : 1, 'LED2' : 2}
        pwm.new_pwm(dic[channel])

    def __del__(self):
        self.stop()
    def start(self):
        """Start PWM."""
        pwm.start()

    def stop(self):
        """Stop PWM."""
        pwm.stop()

    def error(self):
        """Error."""
        if self.status is True:
            self.status = False
            pwm.rate(10)

    def normal(self):
        """Normal."""
        if self.status is False:
            self.status = True
            pwm.rate(1)
