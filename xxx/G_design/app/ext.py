# 扩展库文件
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def init_ext(app):
    db.init_app(app)
    # 加载迁移扩展库，为迁移数据库使用
    migrate.init_app(app, db)
