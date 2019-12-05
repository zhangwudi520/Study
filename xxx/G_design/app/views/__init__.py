from .user import ub
from .test11 import pe
from .about import ab
from .blog import bb
from .share import sb


def init_view(app):
    # 蓝图注册
    app.register_blueprint(ub)
    app.register_blueprint(pe)
    app.register_blueprint(ab)
    app.register_blueprint(bb)
    app.register_blueprint(sb)
