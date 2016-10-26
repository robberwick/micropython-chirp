import time
import ustruct

# To read the capacitance, read 2 bytes from register 0
GET_CAPACITANCE = 0x00
# To change the I2C address of the sensor, write a new address
# (one byte [1..127]) to register 1; the new address will
# take effect after reset
SET_ADDRESS = 0x01
GET_ADDRESS = 0x02
# To read light level, start measurement by writing 3 to the device I2C address
# wait for 3 seconds, read 2 bytes from register 4
MEASURE_LIGHT = 0x03
GET_LIGHT = 0x04
# To read temperature, read 2 bytes from register 5
GET_TEMPERATURE = 0x05
# To reset the sensor, write 6 to the device I2C address.
RESET = 0x06
# To read version, read 1 byte from register 7
GET_VERSION = 0x07
# Sleep mode is  not implemented
SLEEP = 0x08
# To read busy state, read 1 byte from register 9
# Busy = 1, Idle = 0
GET_BUSY = 0x09


class Chirp:
    def __init__(self, i2c, address=0x20):
        self.i2c = i2c
        self.address = address

    def _register_16(self, register, value=None):
        if value is None:
            data = self.i2c.readfrom_mem(self.address, register, 2)
            return ustruct.unpack('>H', data)[0]
        data = ustruct.pack('>H', value)
        self.i2c.writeto_mem(self.address, register, data)

    def _register_8(self, register, value=None):
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        data = ustruct.pack('>B', value)
        self.i2c.writeto_mem(self.address, register, data)

    def reset(self):
        """Reset the sensor"""
        # To reset the sensor, write 6 to the device I2C address.
        self._register_8(SET_ADDRESS, 6)

    def moisture(self):
        """Read the soil moisture capacitance"""
        # To read soil moisture, read 2 bytes from register 0
        return self._register_16(GET_CAPACITANCE)

    def light_level(self):
        """Read the ambient light level"""
        # To read light level, start measurement by writing 3
        # to the device I2C address
        # wait for 3 seconds, read 2 bytes from register 4
        self._register_8(MEASURE_LIGHT, 3)
        time.sleep(3)
        return self._register_16(GET_LIGHT)

    def temperature(self, raw=False):
        """Read the ambient temperatur"""
        # To read temperature, read 2 bytes from register 5
        temp = self._register_16(GET_TEMPERATURE)
        # temp is measured in 1/10ths of a degree centigrade
        # return the raw or adjusted value as required
        return temp if raw else float(temp) / float(10)

    def change_address(self, value=0x20):
        """Change the device i2c address"""
        # To change the I2C address of the sensor, write a new address
        # (one byte [1..127]) to register 1; the new address will
        # take effect after reset
        self._register_8(SET_ADDRESS, value)

        # reset for changes to take effect
        self.reset()

    def busy(self):
        """Return the busy state of the sensor"""
        return self._register_16(GET_BUSY)

    def version(self):
        """Return the version of the sensor firmware"""
        return self._register_16(GET_VERSION)
