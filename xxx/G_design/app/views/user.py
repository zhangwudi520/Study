from flask import Blueprint, jsonify, redirect, request, abort, render_template, Response, session

ub = Blueprint('ub', __name__)


@ub.route('/')
def home():
    return "Flask Success"


@ub.route('/register/', methods=['POST'])
def register():
    data = {
        "username": "xxxx",
        "pwd": "aaaaaa"
    }
    return jsonify(msg="OK", data=data)


@ub.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.form
        user = data.get('uu')
        pwd = data.get('pp')

        print(user, pwd)
        # cookie的使用
        response = Response("{} Login Success".format(user))
        # response.set_cookie('user', user)
        session['user'] = user

        return response


@ub.route('/mine/')
def mine():
    # cookie = request.cookies.get('user')
    user = session.get('user')

    return "{}".format(user)


# 每个views视图都可以添加多个路由
@ub.route('/test/<int:id>/')
@ub.route('/test1/<string:id>/')
def tt(id):
    print(id)
    print(type(id))

    return "{}".format(id)


@ub.route('/redirect/')
def red():
    """[summary]

    Returns:
        [type] -- [description]
    """
    # 重定向
    # return redirect('/')
    # 反向解析
    return redirect(url_for("ub.home"))


@ub.route('/sendrequest/', methods=['GET', 'POST'])
def send_request():
    # print(request.args)
    # print(type(request.args))

    # print(request.form)
    # print(type(request.form))
    abort(404)
    # 强制抛出错误，终止请求

    return "Send Success"


@ub.errorhandler(404)
def handler_error(error):
    print(error)
    # 捕获异常

    return redirect('/')
