import asyncio
import time

from enum import IntEnum

from bleak import BleakClient, discover


class PyHatchBabyRestSound(IntEnum):
    none = 0
    stream = 2
    noise = 3
    dryer = 4
    ocean = 5
    wind = 6
    rain = 7
    bird = 9
    crickets = 10
    brahms = 11
    twinkle = 13
    rockabye = 14


class PyHatchBabyRest(object):
    COLOR_GRADIENT = (254, 254, 254)  # setting this color turns on Gradient mode

    def __init__(self, *args, **kwargs):
        self.device = self.get_hatch_device()
        self._char_tx = "02240002-5efd-47eb-9c1a-de53f7a2b232"
        self._char_feedback = "02260002-5efd-47eb-9c1a-de53f7a2b232"
        self.client = BleakClient(self.device)

        # self._refresh_data()

    @staticmethod
    def get_hatch_device():
        devices = discover()
        for device in devices:
            if device.name == "Hatch Rest":
                return device

    async def send_command(self, command):
        await self.client.write_gatt_char(
            char_specifier=self._char_tx,
            data=bytearray(command, "utf-8"),
            response=True,
        )
        time.sleep(0.25)
        self._refresh_data()

    async def _refresh_data(self):
        response = [hex(x) for x in await self.client.read_gatt_char(self._char_feedback)]

        # Make sure the data is where we think it is
        assert response[5] == "0x43"  # color
        assert response[10] == "0x53"  # audio
        assert response[13] == "0x50"  # power

        red, green, blue, brightness = [int(x, 16) for x in response[6:10]]

        sound = PyHatchBabyRestSound(int(response[11], 16))

        volume = int(response[12], 16)

        power = not bool(int("11000000", 2) & int(response[14], 16))

        self.color = (red, green, blue)
        self.brightness = brightness
        self.sound = sound
        self.volume = volume
        self.power = power

    async def disconnect(self):
        await self.device.disconnect()

    async def power_on(self):
        command = "SI{:02x}".format(1)
        await self._send_command(command)

    async def power_off(self):
        command = "SI{:02x}".format(0)
        await self._send_command(command)

    async def set_sound(self, sound):
        command = "SN{:02x}".format(sound)
        await self._send_command(command)

    async def set_volume(self, volume):
        command = "SV{:02x}".format(volume)
        await self._send_command(command)

    async def set_color(self, red, green, blue, rgb=None):
        await self._refresh_data()

        command = "SC{:02x}{:02x}{:02x}{:02x}".format(red, green, blue, self.brightness)
        await self._send_command(command)

    async def set_brightness(self, brightness):
        await self._refresh_data()

        command = "SC{:02x}{:02x}{:02x}{:02x}".format(
            self.color[0], self.color[1], self.color[2], brightness
        )
        await self._send_command(command)

    @property
    def connected(self):
        return self.device._connected


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete

    rest = PyHatchBabyRest()

    r(rest.power_on())
    r(rest.power_off())
