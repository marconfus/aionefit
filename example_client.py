from aionefit import NefitCore
import asyncio
from pprint import pprint
import logging
from secrets import SERIAL_NUMBER, ACCESS_KEY, PASSWORD


async def main(loop):

    def parse_recursive(msg):
        if 'type' in msg and msg['type'] == 'refEnum':
            for reference in msg['references']:
                client.get(reference['id'])
        else:
            pprint(msg)

    def parse_message(msg):
        pprint(msg)

    client = NefitCore(serial_number=SERIAL_NUMBER,
                       access_key=ACCESS_KEY,
                       password=PASSWORD,
                       message_callback=parse_message)

    loop.nefitclient = client

    await client.xmppclient.connected_event.wait()

    client.get('/ecus/rrc/uiStatus')
    await client.xmppclient.message_event.wait()
    # client.put_value('/heatingCircuits/hc1/usermode', 'manual')
    # client.set_temperature(22)
    # client.get('/heatingCircuits/hc1/manualTempOverride/status')
    # cause "400 Bad Request"
    # client.get('/ecus/rrc/ppm')

    # client.get('/')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(module)s/%(funcName)s : ' +
                        '%(message)s')
    logging.getLogger('aionefit').setLevel(logging.DEBUG)

    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.nefitclient.disconnect()
        loop.close()
