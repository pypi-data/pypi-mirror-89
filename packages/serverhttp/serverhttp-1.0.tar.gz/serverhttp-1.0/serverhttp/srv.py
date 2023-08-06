import datetime, time, threading
from .http.request_parsing import Request
from .http.responses import Response
from .http.formats import reply_format
from .http.parse_time import gettime as _gettime
from .http.environ import get_environ
from io import StringIO
import traceback, asyncio
class ThreadedHTTPServer:
    def __init__(self, name='', app=None):
        self.server = 'python-httpserver/0.2'
        self.functions = {}
        self.threads = []
        self.reply_format = reply_format
        if app:
            self.app = app
            self.app.server = self.server
            self.name = self.app.name
            self.app.prepare_for_deploy(self)
        else:
            if name != '':
                raise Exception('name == \'\'')
            self.name = name
    def _serve_one_client(self, conn, addr):
        import time
        reply_format = self.reply_format
        timeout = 0.1
        while True:
            txt = conn.recv(65535).decode()
            if not txt:
                time.sleep(timeout)
                if timeout > 10:
                    conn.close()
                    return
                timeout += 0.1
                continue
            req = Request(txt)
            reply, reply_obj = self._handle_request(req)
            print(addr[0], '-', '"'+req.text+'"', '-', reply_obj.status)
            conn.sendall(reply)
    def _404(self, env):
        return Response('404 Not Found', 'text/html', '<h1>404 not found')
    def _handle_request(self, request):
        splitted = request.text.split()
        print(splitted)
        env = get_environ(request)
        try:
            path = splitted[1].split('?')[0]
        except:
            path = splitted[1]
        method = splitted[0]
        try:
            res = self.functions[path][method]
        except KeyError:
            res = self._404
        try:
            res = res(env)
        except BaseException as e:
            if __debug__:
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
        threads_append = self.threads.append
        import socket
        s = socket.socket()
        s.bind((host, port))
        print('* Serving App {}'.format(self.name))
        print('* Serving On http://{host}:{port}'.format(host=host, port=port))
        print('* Press <CTRL-C> To Quit')
        self_serve_one_client = self._serve_one_client
        s.listen()
        try:
            while True:
                conn, addr = s.accept()
                t = threading.Thread(target=self_serve_one_client, args=(conn, addr))
                t.daemon = True
                threads_append(t)
                t.start()
        except:
            return

class AsyncHTTPServer:
    def __init__(self, name='', app=None):
        self.server = 'python-httpserver/0.2'
        self.functions = {}
        self.threads = []
        self.reply_format = reply_format
        if app:
            self.app = app
            self.app.server = self.server
            self.name = self.app.name
            self.app.prepare_for_deploy(self)
        else:
            if name != '':
                raise Exception('name == \'\'')
            self.name = name
    @asyncio.coroutine
    def _serve_one_client(self, reader, writer):
        import time
        addr = writer.get_extra_info('peername')
        reply_format = self.reply_format
        timeout = 0.1
        try:
            while True:
                txt = yield from reader.read(65535)
                txt = txt.decode()
                if not txt:
                    break
                req = Request(txt)
                reply, reply_obj = self._handle_request(req)
                print(addr[0], '-', '"'+req.text+'"', '-', reply_obj.status)
                writer.write(reply)
                yield from writer.drain()
            writer.close()
            return
        except:
            writer.close()
            return
    def _404(self, env):
        return Response('404 Not Found', 'text/html', '<h1>404 not found')
    def _handle_request(self, request):
        splitted = request.text.split()
        env = get_environ(request)
        try:
            path = splitted[1].split('?')[0]
        except:
            path = splitted[1]
        method = splitted[0]
        try:
            res = self.functions[path][method]
        except KeyError:
            res = self._404
        try:
            res = res(env)
        except BaseException as e:
            if __debug__:
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
        coro = asyncio.start_server(self._serve_one_client, host=host, port=port, loop=loop)
        srv = loop.run_until_complete(coro)
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

if __name__ == '__main__':
    s = AsyncHTTPServer()
    def test(environ):
        return Response('200 OK', 'text/html', '<h1>Hello</h1>')
    s.functions['/hello'] = {'GET':test}
    s.serve_forever('127.0.0.1', 60000)


