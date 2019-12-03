from .user import ub
from .test11 import pe


def init_view(app):
    # 蓝图注册
    app.register_blueprint(ub)
    app.register_blueprint(pe)
