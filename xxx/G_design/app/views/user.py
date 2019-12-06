from flask import (Blueprint, Response, abort, jsonify, redirect,
                   render_template, request, session)
from sqlalchemy.exc import IntegrityError

from ..models import User, db

ub = Blueprint('ub', __name__, url_prefix='/user')


@ub.route('/')
def home():
    return render_template('bootstrap_demo/base.html')


@ub.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    name = data.get('name', '')
    if not all([name, username, password]):
        return jsonify(msg="参数不全", code=4004)
    try:
        user = User(name=name, user=username)
        user.password = password
        db.session.add(user)
        db.session.commit()

        return jsonify(msg="OK", code=2000)
    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示账号出现了重复值，即账号已注册过
        # current_app.logger.error(e)
        return jsonify(msg="帐号已存在。", code=4005)
    except Exception as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # current_app.logger.error(e)
        return jsonify(msg="Error", code=4000)


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
