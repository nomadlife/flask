from flask import Flask, g, request, Response, make_response
from flask import session, render_template
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True

app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME = 'pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)

@app.route("/tmpl")
def t():
    return render_template('index.html', title="TITLE")


@app.route('/wc')
def wc():
    key = request.args.get("key")
    val = request.args.get('val')
    res = Response("Set COOKIE")
    res.set_cookie(key,val)
    session['Token'] = '123X'
    return make_response(res)

@app.route('/rc')
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return "cookie['" + key + "] = " + val + ' , ' + session.get('Token')

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"




# request environment

@app.route('/reqenv')

def reqenv():
    return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
    'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
    'PATH_INFO: %(PATH_INFO) s <br>'
    'QUERY_STRING: %(QUERY_STRING) s <br>'
    'SERVER_NAME: %(SERVER_NAME) s <br>'
    'SERVER_PORT: %(SERVER_PORT) s <br>'
    'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
    'wsgi.version: %(wsgi.version) s <br>'
    'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
    'wsgi.input: %(wsgi.input) s <br>'
    'wsgi.errors: %(wsgi.errors) s <br>'
    'wsgi.multithread: %(wsgi.multithread) s <br>'
    'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
    'wsgi.run_once: %(wsgi.run_once) s') % request.environ


# request parameter

def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

# app.config['SERVER_NAME'] = 'local.com:5000'

# @app.route("/sd")
# def helloworld_local():
#     return "Hello local.com"

# @app.route("/sd", subdomain="g")
# def helloworld3():
#     return "Hello G.local.com!!!"



@app.route('/rp')
def rp():
    # q = request.args.get('q')
    q = request.args.getlist('q')
    return "q= %s" % str(q)



@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type','text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 ok', headers)
        return [body]
    return make_response(application)



#@app.before_first_request #처음 요청때 무조건 실행
# @app.before_request # 매번 실행 , 모델이 처리하기 전에 .웹필터 역할. ex:url인코딩->디코딩. 
# def before_request():
#     print("before requesting")
#     g.str = "한글2"
    
#@app.after_request # 요청 처리후, 리스폰스 나가기 직전에. ex)DB클로즈
    
#@app.teardown_request # 응답후 실행
    
#@app.teardown_appcontext # ex.오류시에 오류처리.



@app.route("/res1")
def res1():
    custom_res = Response("custom response", 201, {'test':'ttt'})
    return make_response(custom_res)

@app.route("/gg")
def helloworld2():
    return "hello world" + getattr(g,'str','111')

@app.route("/")
def helloworld():
    return "Hello flask !!!"
    
