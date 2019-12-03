from flask import Blueprint, jsonify, redirect

ub = Blueprint('ub', __name__)


@ub.route('/')
def home():
    return "Flask Success"


@ub.route('/login/', methods=['POST'])
def register():
    data = {
        "username": "xxxx",
        "pwd": "aaaaaa"
    }
    return jsonify(msg="OK", data=data)


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
