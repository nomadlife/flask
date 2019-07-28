from flask import Flask, g, Response, make_response

app = Flask(__name__)
app.debug = True



#@app.before_first_request #처음 요청때 무조건 실행
@app.before_request # 매번 실행 , 모델이 처리하기 전에 .웹필터 역할. ex:url인코딩->디코딩. 
def before_request():
    print("before requesting")
    g.str = "한글2"
    
#@app.after_request # 요청 처리후, 리스폰스 나가기 직전에. ex)DB클로즈
    
#@app.teardown_request # 응답후 실행
    
#@app.teardown_appcontext # ex.오류시에 오류처리.



@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type','text/plain'),
                   ('Content-Length', str(len(body)))]
        start_response('200 ok', headers)
        return [body]
    return make_response(application)






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
    
