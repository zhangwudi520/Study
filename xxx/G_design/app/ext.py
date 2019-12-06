# 扩展库文件
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    # 加载迁移扩展库，为迁移数据库使用
    migrate.init_app(app, db)
    Session(app)
    Bootstrap(app)
    DebugToolbarExtension(app)
