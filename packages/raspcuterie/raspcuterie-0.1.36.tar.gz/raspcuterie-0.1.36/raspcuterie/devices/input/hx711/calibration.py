"""
HX711 Load cell amplifier Python Library
Original source: https://gist.github.com/underdoeg/98a38b54f889fce2b237
Documentation source: https://github.com/aguegu/ardulibs/tree/master/hx711
Adapted by 2017 Jiri Dohnalek

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import sys
import time

from raspcuterie.devices.input.hx711 import HX711
from raspcuterie.gpio import GPIO


hx = HX711("weight")


def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    print("Initializing.\n Please ensure that the scale is empty.")
    scale_ready = False
    while not scale_ready:
        if GPIO.input(hx.DOUT) == 0:
            scale_ready = False
        if GPIO.input(hx.DOUT) == 1:
            print("Initialization complete!")
            scale_ready = True


def calibrate():
    input("Remove any items from scale. Press any key when ready.")
    offset = hx.read_average()
    print("Value at zero (offset): {}".format(offset))
    hx.offset = offset
    print("Please place an item of known weight on the scale.")

    input("Press any key to continue when ready.")
    measured_weight = hx.read_average() - hx.offset
    item_weight = input("Please enter the item's weight in grams.\n>")
    scale = int(measured_weight) / int(item_weight)
    hx.scale = scale
    print("Scale adjusted for grams: {}".format(scale))


def loop():
    """
    code run continuously
    """
    try:
        prompt_handled = False
        while not prompt_handled:
            val = hx.get_grams()
            hx.power_down()
            time.sleep(0.001)
            hx.power_up()
            print("Item weighs {} grams.\n".format(val))
            choice = input(
                "Please choose:\n"
                "[1] Recalibrate.\n"
                "[2] Display offset and scale and weigh an item!\n"
                "[0] Clean and exit.\n>"
            )
            if choice == "1":
                calibrate()
            elif choice == "2":
                print("\nOffset: {}\nScale: {}".format(hx.offset, hx.scale))
            elif choice == "0":
                prompt_handled = True
                cleanAndExit()
            else:
                print("Invalid selection.\n")
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


if __name__ == "__main__":

    setup()
    calibrate()
    while True:
        loop()
