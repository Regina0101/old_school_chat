import asyncio
import logging
from datetime import datetime

import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
import json
import main
from aiofile import async_open

logging.basicConfig(level=logging.INFO)

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            await asyncio.gather(*(client.send(message) for client in self.clients))

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)


    async def log_to_file(self, user_name, date, time):
        async with async_open("log.txt", "a" ) as file:
            await file.write(f"{user_name} executed 'exchange' command on {date} at {time} \n")

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            parts = message.split()
            if len(parts) == 2 and parts[0] == "exchange" and parts[1].isdigit():
                days = int(parts[1])
                exchange = await main.get_currency_rate(days)
                await self.send_to_clients(json.dumps(exchange, indent=4, ensure_ascii=False))
                await self.log_to_file(ws.name, datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime("%H:%M:%S.%f")[:-6])
            elif message == 'Hello server':
                await self.send_to_clients("Привіт мої карапузи!")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")

async def server_start():
    server = Server()
    async with websockets.serve(server.ws_handler, '0.0.0.0', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(server_start())
