"""
module for time
"""
import machine
import utime

from userv import swagger
from userv.routing import json_response
from .logging import grown_log

try:
    import uasyncio as asyncio
except ImportError:
    import asyncio
try:
    import usocket as socket
except ImportError:
    import socket
try:
    import ustruct as struct
except ImportError:
    import struct

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "pool.ntp.org"


def _set_system_time(ntp_time):
    """
    There's currently no timezone support in MicroPython, so
    utime.localtime() will return UTC time (as if it was .gmtime())
    """
    tm = utime.localtime(ntp_time)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    grown_log.info("timesync: %s" % str(utime.localtime()))


async def _time_from_server():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA


async def _time_sync_task(time_between_syncs_s=300):
    """
    task for synchronising time
    """
    while True:
        try:
            server_time = await _time_from_server()
            _set_system_time(server_time)
        except Exception as e:
            grown_log.error("time_control: %s" % str(e))

        await asyncio.sleep(time_between_syncs_s)


def seconds_for_one_day(time_s):
    """
    strips away all seconds not in one day
    :param time_s:
    :return:
    """
    return time_s % (60 * 60 * 24)


def get_current_time():
    """
    retuns the current hh:mm:ss in seconds
    :rtype: int
    """
    current_time = utime.time()
    return seconds_for_one_day(current_time)


@swagger.info("Returns current time information of device")
async def _get_time_information(request):
    current_time = utime.time()
    return json_response({
        'time_s': current_time,
        'time_of_day_s': seconds_for_one_day(current_time)
    })


def add_time_control(router):
    """
    Adds an continues sync process to an server
    also adds routes to serve certain data
    :type router: user.routing.Router
    """
    grown_log.info('Adding time control to grown server')
    try:
        # create lighting task based on set settings
        loop = asyncio.get_event_loop()
        loop.create_task(_time_sync_task())
        # create subserver for light control
        router.add("/rest/time", _get_time_information, 'GET')
    except Exception as e:
        grown_log.error("time_control: %s" % str(e))
