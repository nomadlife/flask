from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.debug = True
app.jinja_env.trim_blocks = True



app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME = 'pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)

@app.route('/top200')
def top200():
    return render_template('application.html', title="app MAIN!!")

# @app.route('/top102')
# def top102():
#     return render_template('application2.html', title="MAIN2!!")

class FormInput :    def __init__(self, id, name, value, checked, text):
        self.id = id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text
        self.type = type
        
@app.route('/top100')
def top100():
    rds = []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i==2:
            checked = 'checked'
        text = 'RadioTest' + str(i)
        rds.append(FormInput(id, name, value, checked, text))
    return render_template('app.html', title="MAIN!!", ttt="testTTT", radioList=rds)

@app.route('/main')
def main():
    return render_template('main.html', title='MAIN!!') 


class Nav:
    def __init__(self, title, url='#', children=[]):
        self.title = title
        self.url = url
        self.children = children 

@app.route('/tmpl3')
def tmpl3():
    py = Nav("파이썬", "localhost:5000/")
    java = Nav("자바", "localhost:5000/")
    t_prg = Nav("프로그래밍 언어", "localhost:5000/", [py, java])
    
    jinja = Nav("jinja", "localhost:5000/")
    gc = Nav("Genshi, Cheetah", "localhost:5000/")
    flask = Nav("플라스크", "localhost:5000/", [jinja, gc])
    
    spr = Nav("스프링", "localhost:5000/")
    ndjs = Nav("노드js", "localhost:5000/")
    t_webf = Nav("웹 프레임워크", "localhost:5000/", [flask, spr, ndjs])
    
    my = Nav("나의 일상", "localhost:5000/")
    issue = Nav("이슈 게사판", "localhost:5000/")
    t_others = Nav("기타", "localhost:5000/", [my, issue])
    return render_template("index.html", navs=[t_prg, t_webf, t_others])


@app.route('/tmpl2')
def tmpl2():
    a = (1,"만남1","김건모",False, [])
    b = (2,"만남2","노사연",True, [a])
    c = (3,"만남3","익명",False, [a,b])
    d = (4,"만남4","익명",False, [a,b,c])
    
    return render_template("index.html", lst2=[a,b,c,d])
    

@app.route("/tmpl")
def t():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    print("h=", h)
    
    lst = [("만남1","김건모"),("만남2","노사연"),("만남3","노사봉")]
    return render_template('index.html', title=tit, mu = h, lst = lst)


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
    
