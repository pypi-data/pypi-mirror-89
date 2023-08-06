from serverhttp import *
app_resp = '''\
<?xml version="1.0">
<text>Hello World!</text>'''
demo_app = app.App('demo')
@app.route('/', methods=['GET'])
def demo_app_hello(request):
    return Response('200 OK', 'application/rss+xml', )
serv = srv.AsyncHTTPServer(app=demo_app)

