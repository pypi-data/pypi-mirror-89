import datetime, time, threading
from ..http.request_parsing import Request
from ..http.responses import Response
from ..http.formats import reply_format
from ..http.parse_time import gettime as _gettime
from ..http.environ import get_environ
from .version import version
from io import StringIO
import traceback
class ThreadedHTTPServer:
    def __init__(self, name='', app=None, max_threads=2000, debug=False， sslcontext=None):
        self.server = version
        self.functions = {}
        self.threads = []
        self.max_threads=max_threads
        self.reply_format = reply_format
        self._debug_=debug
        if app:
            self.app = app
            self.app.server = self.server
            self.name = self.app.name
            self.app.prepare_for_deploy(self)
        else:
            self.name = name
        self.sslcontext=sslcontext
    def _serve_one_client(self, conn, addr):
        import time
        reply_format = self.reply_format
        timeout = 0.1
        conn = self.sslcontext.wrap_socket(conn, server_side=True)
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
    def _405(self, env):
        return Response('405 Method Not Allowed')
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
            res = self.functions[path]
        except KeyError:
            res = self._404
        try:
            res = res[method]
        except:
            res = self._405
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
        threads_append = self.threads.append
        import socket
        s = socket.socket()
        s.bind((host, port))
        if self.name != '':
            print('* Serving App {}'.format(self.name))
        print('* Serving On http://{host}:{port}'.format(host=host, port=port))
        print('* Press <CTRL-C> To Quit')
        self_serve_one_client = self._serve_one_client
        s.listen()
        try:
            while True:
                if len(self.threads)>self.max_threads:
                    continue
                tup = s.accept()
                t = threading.Thread(target=self_serve_one_client, args=tup)
                t.daemon = True
                threads_append(t)
                t.start()
        except:
            return

