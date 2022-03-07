import asyncio
import websockets


async def observer(url):
    async with websockets.connect(url) as ws:
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=20)
                print('Message in : {}'.format(msg))
            except asyncio.TimeoutError:
                # No data in 20 seconds, check the connection.
                try:
                    pong_waiter = await ws.ping()
                    await asyncio.wait_for(pong_waiter, timeout=10)
                except asyncio.TimeoutError:
                    # No response to ping in 10 seconds, disconnect.
                    break


if __name__ == '__main__':
    # host = 'ws://scada.p-enterprise.com/ws/stream/chat/'
    host = 'ws://192.168.1.40:6789/stream'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(observer(host))
