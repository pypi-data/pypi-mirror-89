import asyncio
import sys
import time

from collections import namedtuple
from enum import IntEnum

from bleak import BleakClient, discover

HATCH_TX_UUID = "02240002-5efd-47eb-9c1a-de53f7a2b232"
HATCH_FEEDBACK_UUID = "02260002-5efd-47eb-9c1a-de53f7a2b232"


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


async def get_hatch_device():
    devices = await discover()
    for device in devices:
        if device.name == "Hatch Rest":
            return device


async def get_services(device):
    async with BleakClient(device) as client:
        return await client.get_services()


async def get_hatch_chars(device):
    tx_char = None
    feedback_char = None

    async with BleakClient(device) as client:
        for service in await client.get_services():
            for characteristic in service.characteristics:
                if characteristic.uuid == HATCH_TX_UUID:
                    tx_char = characteristic
                elif characteristic.uuid == HATCH_FEEDBACK_UUID:
                    feedback_char = characteristic

                if tx_char and feedback_char:
                    break

    return (tx_char, feedback_char)


async def send_command(device, command):
    async with BleakClient(device) as client:
        await client.write_gatt_char(
            char_specifier=HATCH_TX_UUID,
            data=bytearray(command, "utf-8"),
            response=True,
        )


async def power_on(device):
    await send_command(device, "SI{:02x}".format(1))


async def set_volume(device, volume):
    await send_command(device, "SV{:02x}".format(volume))


async def power_off(device):
    await send_command(device, "SI{:02x}".format(0))


async def read_feedback(device, char):
    async with BleakClient(device) as client:
        return await client.read_gatt_char(
            char_specifier=char,
        )


async def get_all_chars(device):
    chars = []
    async with BleakClient(device) as client:
        for service in await client.get_services():
            for characteristic in service.characteristics:
                if "read" in characteristic.properties:
                    chars.append(
                        (characteristic, await client.read_gatt_char(characteristic))
                    )

    return chars


async def get_status(device):
    async with BleakClient(device) as client:

        raw_char_read = await client.read_gatt_char(HATCH_FEEDBACK_UUID)

    status_hex = [hex(x) for x in raw_char_read]

    # Make sure the data is where we think it is
    assert status_hex[5] == "0x43"  # color
    assert status_hex[10] == "0x53"  # audio
    assert status_hex[13] == "0x50"  # power

    red, green, blue, brightness = [int(x, 16) for x in status_hex[6:10]]
    sound = PyHatchBabyRestSound(int(status_hex[11], 16))

    volume = int(status_hex[12], 16)

    power = not bool(int("11000000", 2) & int(status_hex[14], 16))

    status = namedtuple(
        "HatchStatus",
        ["red", "green", "blue", "brightness", "sound", "volume", "power"],
    )

    return status(
        red=red,
        green=green,
        blue=blue,
        brightness=brightness,
        sound=sound,
        volume=volume,
        power=power,
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    r = loop.run_until_complete
    hatch_device = r(get_hatch_device())

    import ipdb; ipdb.set_trace()

    if hatch_device is None:
        print("Could not find hatch device.")
        sys.exit(1)
    else:
        print(hatch_device)

    services = r(get_services(hatch_device))

    for service in services:
        print("Service: ", service.description)
        for characteristic in service.characteristics:
            print("  Characteristic: ", characteristic.description)
            print("    Characteristic UUID: ", characteristic.uuid)

    # tx_char, feedback_char = r(get_hatch_chars(hatch_device))

    # print(r(read_feedback(hatch_device, feedback_char)))

    # all_chars = r(get_all_chars(hatch_device))
    # for char in all_chars:
    #     print(char[0], char[1])

    # print(tx_char)
    # print(feedback_char)

    print(r(get_status(hatch_device)))
    print("powering on")
    print(r(power_on(hatch_device)))
    # time.sleep(5)

    print(r(get_status(hatch_device)))
    print("Setting volume high")
    print(r(set_volume(hatch_device, 150)))
    time.sleep(5)

    print(r(get_status(hatch_device)))
    print("Setting volume down")
    print(r(set_volume(hatch_device, 10)))
    time.sleep(5)

    print(r(get_status(hatch_device)))
    print("powering off")
    print(r(power_off(hatch_device)))

    status = r(get_status(hatch_device))
    print(status)

    # r(power_on(hatch_device, HATCH_TX_UUID))

    # import ipdb

    # ipdb.set_trace()
