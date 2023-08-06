#    Prana RC
#    Copyright (C) 2020 Dmitry Berezovsky
#    
#    prana is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    prana is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio

from sizzlews.client.common import RPCInvocationError

from prana_rc.contrib.api import SetStateDTO
from prana_rc.contrib.client.aiohttp import PranaRCAioHttpClient

from prana_rc.entity import Speed

client = PranaRCAioHttpClient("http://orion:8881/")
# client = PranaRCAioHttpClient("http://localhost:8881/")

class EnumsConfig:
    use_enum_values = True

async def main():
    async with client:
        try:
            # b = SetStateDTO(speed=4)
            # # b.Config = EnumsConfig
            # print(b.json())
            # b = b.dict()
            # print(b)
            # a = SetStateDTO(speed=4).dict()
            # print(a)
            print(await client.get_state("00:A0:50:99:52:D2"))
            print(await client.set_state("00:A0:50:99:52:D2", SetStateDTO(speed=Speed.OFF)))
        # except RPCInvocationError as e:
        except Exception as e:
            print("Error: " + str(e))
        # try:
        #     print(await client.my_dto_method())
        # except Exception as e:
        #     print(e)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
