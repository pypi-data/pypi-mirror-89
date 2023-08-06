import datetime, time, threading
from ..http_support.request_parsing import Request
from ..http_support.responses import Response
from ..http_support.formats import reply_format
from ..http_support.parse_time import gettime as _gettime
from ..http_support.environ import get_environ
from .version import version
from io import StringIO
import traceback, sys
if float(sys.version[:3]) < 3.7:
    raise DeprecationWarning('python version not supported')
import asyncio

class AsyncHTTPServer:
    def __init__(self, name='', app=None, debug=False, sslcontext=None):
        self._debug_=debug
        self.server = version
        self.functions = {}
        self.threads = []
        self.reply_format = reply_format
        if app:
            self.app = app
            self.app.server = self.server
            self.name = self.app.name
            self.app.prepare_for_deploy(self)
        else:
            self.name = name
        self.sslcontext=sslcontext
    
    async def _serve_one_client(self, reader, writer):
        import time
        addr = writer.get_extra_info('peername')
        reply_format = self.reply_format
        timeout = 0.1
        try:
            while True:
                txt = await reader.read(65535)
                txt = txt.decode()
                if not txt:
                    await asyncio.sleep(timeout)
                    timeout += 0.1
                    if timeout > 10:
                        break
                    continue
                req = Request(txt)
                reply, reply_obj = self._handle_request(req)
                print(addr[0], '-', '"'+req.text+'"', '-', reply_obj.status)
                writer.write(reply)
                await writer.drain()
            writer.close()
            return
        except:
            writer.close()
            return
    def _404(self, env):
        return Response('404 Not Found', 'text/html', '<h1>404 not found')
    def _405(self, env):
        return Response('405 Method Not Allowed')
    def _handle_request(self, request):
        splitted = request.text.split()
        env = get_environ(request)
        try:
            path = splitted[1].split('?')[0]
        except:
            path = splitted[1]
        method = splitted[0]
        try:
            res = self.functions[path]
        except KeyError:
            res = self._404
        try:
            res = res[method]
        except:
            if res == self._404:
                pass
            else: res = self._405
        try:
            res = res(env)
        except BaseException as e:
            if self._debug_:
                i = StringIO()
                traceback.print_exc(file=i)
                traceback.print_exc()
                i.seek(0)
                d = i.read()
                res = Response('500 Server Error', 'text/plain', '500 server error:\r\n'+d)
            else:
                res = Response('500 Server Error', 'text/plain', '500 server error')
        reply = str(res).encode()
        return reply, res
    def serve_forever(self, host, port):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(
            self._serve_one_client, host=host, port=port, loop=loop, ssl=self.sslcontext)
        srv = loop.run_until_complete(coro)
        if self.name:
            print('* Serving App {}'.format(self.name))
        print('* Serving On http://{host}:{port}'.format(host=host, port=port))
        print('* Press <CTRL-C> To Quit')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print('Shutting Down...')
            srv.close()
            loop.run_until_complete(srv.wait_closed())
            loop.close()
            pass

