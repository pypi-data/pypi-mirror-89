# -*- coding: utf-8 -*-
import ast
# import websockets
from aiohttp import web
# import asyncio
from .utils import Client
import json
import logging

_logger = logging.getLogger(__name__)

logging.basicConfig(level='INFO')


class JSON(object):
    def __init__(self, data):
        self.data = data

    def __format__(self, format):
        return json.dumps(self.data, indent=2, sort_keys=True)


frame_template = """
{session}
{event}
{filename}:{lineno}:{source_lineno}
{arg_json}

Locals:
{locals_json}

Globals:
{globals_json}

Code:
{source}
"""

code_template = """
value = 123
value += 2
"""


class DebuggerClient(Client):

    def __init__(self, websocket):
        super(DebuggerClient, self).__init__(websocket)
        self.subscribers = set()

    def subscribe(self, client):
        self.subscribers.add(client)

    def unsubscribe(self, client):
        self.subscribers.remove(client)

    async def on_read(self, dat):
        for client in self.subscribers:
            await client.send_queue.put(dat)

        return

        if dat and dat.get('type') == 'frame':
            dat.update({
                "locals_json": JSON(dat['locals']),
                "globals_json": JSON(dat['globals']),
                "arg_json": JSON(dat['arg']),
            })

            print(frame_template.format(**dat))

        # if 'value' in dat.get('locals'):
        #     msg = {
        #         'action': 'set_locals',
        #         'key': 'value',
        #         'value': 10
        #     }
        #     await self.send_queue.put(msg)

        # if 'value' in dat.get('locals'):
        #     msg = {
        #         'action': 'execute',
        #         'code': code_template
        #     }
        #     await self.send_queue.put(msg)

        def parse_break_line(command):
            _, rest = command.split(' ', 1)
            event, rest = rest.split(' ', 1)
            line, filename = rest.split(' ', 1)

            if ':' in line:
                line = line.split(':', 1)
                line[0] = int(line[0])
                line[1] = int(line[1])
            else:
                line = int(line) if line != 'any' else line

            return [event, line, filename]

        while True:
            command = input("({}) ➜ ".format(self.uuid))

            try:
                if command in [
                    'step', 'continue', 'stop', 'inspect', 'return', 'breakpoints',
                ]:
                    await self.send_queue.put({'action': command})
                    return
                elif command.startswith('set'):
                    _, vals = command.split(' ', 1)
                    key, value = command.split(' ')
                    action = {
                        'action': 'set_locals',
                        'key': key,
                        'value': ast.literal_eval(value)
                    }
                    await self.send_queue.put(action)
                    return
                elif command.startswith('eval'):
                    _, code = command.split(' ', 1)
                    action = {
                        'action': 'execute',
                        'code': code
                    }
                    await self.send_queue.put(action)
                    return
                elif command.startswith('break'):
                    action = {
                        "action": "add_breakpoint",
                        "breakpoint": parse_break_line(command)
                    }
                    await self.send_queue.put(action)
                    return
                elif command.startswith('-break'):
                    action = {
                        "action": "remove_breakpoint",
                        "breakpoint": parse_break_line(command)
                    }
                    await self.send_queue.put(action)
                    return
            except Exception:
                pass


class DebuggingClient(Client):
    def __init__(self, websocket, servers):
        super(DebuggingClient, self).__init__(websocket)
        self.servers = servers

    async def on_read(self, data):
        if data.get('action') == 'list':
            await self.send_queue.put({
                "type": "instances",
                "instances": [
                    {
                        "uuid": server.uuid,
                        "tags": server.tags
                    }
                    for server in
                    self.servers
                ]
            })
        elif data.get('action') == 'subscribe':
            for server in self.servers:
                if server.uuid == data.get('uuid'):
                    server.subscribe(self)
        elif data.get('action') == 'unsubscribe':
            for server in self.servers:
                if server.uuid == data.get('uuid'):
                    server.unsubscribe(self)
        elif data.get('action') == 'call':
            for server in self.servers:
                if server.uuid == data.get('uuid'):
                    await server.send_queue.put(data.get('params'))


debugging_sessions = set()
debugging_clients = set()


def start_aiohttp():

    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        print("New connexion")

        data = await ws.receive_json()
        print(data)

        # if "event" in data:
        #     msg = {
        #         "action": "configure",
        #         "type": "break",
        #         "files": ["test.py"]
        #     }
        #     await ws.send_json(msg)

        if data.get('event') == 'new_session':
            print("Got new debug")
            client = DebuggerClient(ws)
            client.uuid = data.get('uuid')
            client.tags = data.get('tags', [])
            debugging_sessions.add(client)
        elif data.get('event') == 'new_client':
            print("Got new client")
            client = DebuggingClient(ws, debugging_sessions)
            client.uuid = 'client'
            debugging_clients.add(client)

        while True:
            await client.event_loop()
            try:
                if client.stopped:
                    await client.stop()
                    break
            except KeyboardInterrupt:
                await client.on_read(None)

        if isinstance(client, DebuggerClient):
            debugging_sessions.remove(client)
        elif isinstance(client, DebuggingClient):
            debugging_clients.remove(client)

        _logger.info('websocket connection closed')

        return ws

    app = web.Application()
    app.add_routes([web.get('/ws', websocket_handler)])
    web.run_app(app)


def server():
    start_aiohttp()


def parse_break_line(command):
    _, rest = command.split(' ', 1)
    event, rest = rest.split(' ', 1)
    line, filename = rest.split(' ', 1)

    if ':' in line:
        line = line.split(':', 1)
        line[0] = int(line[0])
        line[1] = int(line[1])
    else:
        line = int(line) if line != 'any' else line

    return [event, line, filename]


def parse_command(command):
    if command in [
        'step',
        's',
        'continue',
        'c',
        'stop',
        'inspect',
        'return',
        'interrupt',
        'breakpoints',
        'w',
        'up',
        'down',
    ]:
        return {'action': command}
    elif command.startswith('set'):
        _, vals = command.split(' ', 1)
        key, value = command.split(' ')
        action = {
            'action': 'set_locals',
            'key': key,
            'value': ast.literal_eval(value)
        }
        return action
    elif command.startswith('eval'):
        _, code = command.split(' ', 1)
        action = {
            'action': 'execute',
            'code': code
        }
        return action
    elif command.startswith('break'):
        action = {
            "action": "add_breakpoint",
            "breakpoint": parse_break_line(command)
        }
        return action
    elif command.startswith('-break'):
        action = {
            "action": "remove_breakpoint",
            "breakpoint": parse_break_line(command)
        }
        return action


def format_response(data):
    if data.get('type') == 'frame':
        lineno = data.get('lineno', 0) - data.get('source_lineno', 0)

        source = "\n".join([
            "{}{}".format(
                '->' if index == lineno else '  ',
                line
            )
            for index, line in enumerate(data.get('source').split('\n'))
        ])

        data['source'] = source

        data.update({
            "locals_json": JSON(data['locals']),
            "globals_json": JSON(data['globals']),
            "arg_json": JSON(data['arg']),
        })

        print(frame_template.format(**data))
    elif data.get('type') == 'frames':
        print("Call stack")
        for info in data.get('frames', []):
            print(
                " {filename}:{lineno} in {function}".format(**info)
            )
    elif data.get('type') == 'instances':
        print("Instances")
        for instance in data.get('instances', []):
            print("{uuid}: {tags}".format(**instance))
    elif data.get('type') == 'breakpoints':
        print("Breakpoints")
        for event, line, filename in data.get('breakpoints', []):
            print("Event: {} File: {}:{}".format(event, filename, line))


def client():
    import aiohttp
    import asyncio
    import os

    HOSTNAME = os.environ.get('AWDB_URL', 'wss://awdb.docker/ws')

    async def execute_commands():
        connector = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=connector)
        websocket = await session.ws_connect(HOSTNAME)

        active = None

        await websocket.send_json({
            "event": "new_client"
        })

        while True:
            prompt = "({})".format(active) if active else ""
            command = input("command {}> ".format(prompt))

            action = None
            if not command:
                break

            if command == 'list':
                action = {
                    'action': 'list'
                }
            elif command.startswith('use'):
                active = command.split(' ', 1)[1]
            elif command.startswith('subscribe'):
                active = command.split(' ', 1)[1]
                action = {
                    'action': 'subscribe',
                    'uuid': active
                }
            elif command.startswith('unsubscribe'):
                active = command.split(' ', 1)[1]
                action = {
                    'action': 'unsubscribe',
                    'uuid': active
                }
            else:
                action = parse_command(command)
                if action:
                    action = {
                        'action': 'call',
                        'params': action,
                        'uuid': active
                    }

            if action:
                await websocket.send_json(action)

                while True:
                    read = asyncio.create_task(websocket.receive_json())
                    done, pending = await asyncio.wait({read}, timeout=1)
                    if len(done) > 0:
                        for dd in done:
                            response = await dd
                            format_response(response)
                    else:
                        read.cancel()
                        break

        await websocket.close()

        print("done")

    loop = asyncio.new_event_loop()
    task = loop.create_task(execute_commands())
    loop.run_until_complete(task)
