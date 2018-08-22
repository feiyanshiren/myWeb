# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
"""
服务器程序主入口
"""
#引头
# from gevent import monkey
# monkey.patch_all()
import sys
import imp
import os
path = os.path.split(os.path.realpath(__file__))[0]
if path not in sys.path:
    sys.path.append(path)
# import socket
# from cherrypy import wsgiserver
# from cheroot import wsgi
import traceback

from bottle import request, error, response, route, static_file, run
import bottle


import config
#import web
app = bottle.app()
#更变运行字符环境
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] =\
            'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] =\
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if bottle.request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


class DiySelf():
    def __init__(self, the_conf, the_argument):
        self.settings = {}
        self.settings["config"] = the_conf
        self.argument = the_argument

    def get_argument(self, name, df=None):
        return self.argument.get(name, df)

    def get_cookie(self, name):
        return request.cookies.get(name)

    def set_cookie(self, name, val, path="/"):
        response.set_cookie(name, val)

    def getFiles(self):
        return request.files

    def getBody(self):
        return request.body

    def getIP(self):
        return request.environ.get('REMOTE_ADDR')#@UndefinedVariable @IgnorePep8


#@get('/<name>')
@app.route('/<name>', method=['OPTIONS', 'GET'])
@enable_cors
def theGet(name):
    try:
        #获取url
        method = name
        method = method.replace("/", "")
        mm = imp.load_source(method,
                             config.main_path + "/get/" + method + ".py")
        mtd = getattr(mm, "post")
        diy_self = DiySelf(config, request.params)
        return mtd(diy_self)
    except:
        e = traceback.format_exc()
        return u'{"code":-2,"tip":"未知url","error":"%s","name":"%s"}'\
                    % (str(e), name)


#@post('/<name>')
@app.route('/<name>', method=['OPTIONS', 'POST'])
@enable_cors
def thePost(name):
    try:
        method = name
        method = method.replace("/", "")
        mm = imp.load_source(method,
                        config.main_path + "/post/" + method + ".py")
        mtd = getattr(mm, "post")
        diy_self = DiySelf(config, request.forms)
        return mtd(diy_self)
    except Exception, e:
        print e
        return u'{"code":-2,"tip":"未知url","error":%s}' % (str(e))


@error(404)
def error404(error):
    return 'Nothing here, sorry'


@route('/www/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='www')


config.main_path = os.path.split(os.path.realpath(__file__))[0]

run(host='0.0.0.0', port=8848, server="gevent")
# run(host='0.0.0.0', port=8848)

# application = bottle.default_app()

# application.run(host='0.0.0.0', port=8848)
"""
server = wsgiserver.CherryPyWSGIServer(
    bind_addr=('0.0.0.0', 80),
    wsgi_app=application
    # request_queue_size=500,
    # server_name=socket.gethostname()
)
"""

"""
server = wsgi.Server(
    bind_addr=('0.0.0.0', 80),
    wsgi_app=application
)
"""

# server.start()


