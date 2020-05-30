###
# Copyright (c) 2020, mogad0n
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###
import datetime
from dateutil import tz
import random
import pytz

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Where420')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Where420(callbacks.Plugin):
    """Tells you where it will be 4:20am next"""
    pass

    def where420(self, irc, msg, args):
        """
        tells you where it is 4:20 AM next
        """
        offsets = ['UTC−1100', 'UTC−0800', 'UTC−0700', 'UTC−0600', 'UTC−0500', 'UTC−0100', 'UTC+0000', 'UTC+0100', 'UTC+0200',
               'UTC+0300', 'UTC+0400', 'UTC+0530', 'UTC+0700', 'UTC+0800', 'UTC+0900', 'UTC+1000', 'UTC+1200', 'UTC+1300']
        utc_420timedeltas = {}


        for offset in offsets:

            now = datetime.datetime.now(tz=tz.tzstr(offset))
            today_420 = now.replace(hour=4, minute=20, second=0, tzinfo=tz.tzstr(offset))
            zero_td = datetime.timedelta()
            time_until_today_420 = today_420 - now
            if time_until_today_420 >= zero_td:
                time_until_next_420 = time_until_today_420
            else:
                tomorrow_420 = today_420 + datetime.timedelta(days=1)
                time_until_next_420 = tomorrow_420 - now

            utc_420timedeltas[offset] = time_until_next_420.total_seconds()


        # find the key with the minimum value
        closest_utc = min(utc_420timedeltas, key=lambda k: utc_420timedeltas[k])

        closest_hours = int(closest_utc[3:6])
        closest_min = int(closest_utc[6:8])

        utc_offset = datetime.timedelta(hours=closest_hours, minutes=closest_min)

        tzs420 = [tz.zone for tz in map(pytz.timezone, pytz.all_timezones_set) if now.astimezone(tz).utcoffset() == utc_offset]

        city420 = random.choice(tzs420)
        re = utils.str.format(f'It will be 4:20am next in {city420} in {min(utc_420timedeltas.values())} seconds. _\\|/_ ( .__.) . o O ( smoke weed )')
        irc.reply(re)
    where420 = wrap(where420)

Class = Where420


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
