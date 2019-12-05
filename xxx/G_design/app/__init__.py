from flask import Flask

from .ext import init_ext
from .settings import envs
from .views import init_view
from .models import User


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/G_design"
    # 加载配置
    app.config.from_object(envs.get('develop'))
    # @app.errorhandler(404)
    # def page_not_found(error):
    #     """
    #     捕获全局404异常
    #     """
    #     return "xxx"

    init_ext(app)
    init_view(app)
    # 隐匿函数调用蓝图

    return app
