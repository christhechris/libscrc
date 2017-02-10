# -*- coding:utf8 -*-
""" Apalis T30 PWM."""
# !/usr/bin/python
# Python:   3.5.2
# Platform: i.mx6 ARMv7
# Author:   Heyn
# Program:  ImxPWM.
# History:  2017/02/09

# Toradex Name	NXP/Freescale Name	    sysfs path	            Note
#       PWM1	  PWM1	            /sys/class/pwm/pwmchip0/	-
#       PWM2	  PWM2	            /sys/class/pwm/pwmchip1/	-
#       PWM3	  PWM3	            /sys/class/pwm/pwmchip2/	SD_CLK

import os.path

class ImxPWM:
    """Apalis T30 ImxPWM Class."""

    def __init__(self, channel='PWM1', path='/sys/class/pwm'):
        super(ImxPWM, self).__init__()

        dic = {'PWM1' : '/pwmchip0', 'PWM2' : '/pwmchip1', 'PWM3' : '/pwmchip2'}
        self.path = path + dic[channel]
        self.status = True

        export = open(self.path + '/export', 'w')
        unexport = open(self.path +'/unexport', 'w')

        pwm0_exists = os.path.isdir(self.path + '/pwm0')
        if pwm0_exists and False:
            unexport.write('0')
            unexport.flush()

        if not pwm0_exists or False:
            export.write('0')
            export.flush()

        export.close()
        unexport.close()

        self.periods = open(self.path + '/pwm0/period', 'w')
        self.duty_cycles = open(self.path + '/pwm0/duty_cycle', 'w')

        self.periods.write(str(1000 * 1000 * 1000))
        self.periods.flush()
        self.duty_cycles.write(str(500 * 1000 * 1000))
        self.periods.flush()

        self.pwm = open(self.path + '/pwm0/enable', 'w')

    def __del__(self):
        self.stop()

    def attrs(self, period, duty_cycle):
        """period (ms) & duty_cycle (ms)"""

        # Clear duty_cycle
        self.duty_cycles.seek(0)
        self.duty_cycles.write(str(0))
        self.duty_cycles.flush()

        # Set periods
        self.periods.seek(0)
        self.periods.write(str(period * 1000 * 1000))   # nano seconds
        self.periods.flush()

        # Set duty_cycles
        self.duty_cycles.seek(0)
        self.duty_cycles.write(str(duty_cycle * 1000 * 1000))   # nano seconds
        self.duty_cycles.flush()


    def start(self):
        """Start PWM."""
        self.pwm.write("1")
        self.pwm.flush()

    def stop(self):
        """Stop PWM."""
        self.pwm.write("0")
        self.pwm.flush()

    def error(self):
        """Error."""
        if self.status is True:
            self.status = False
            self.attrs(200, 100)

    def normal(self):
        """Normal."""
        if self.status is False:
            self.status = True
            self.attrs(1000, 500)
