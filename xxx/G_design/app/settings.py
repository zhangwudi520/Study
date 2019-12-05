import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_info(db_info):
    e = db_info.get('ENGINE') or "mysql"
    d = db_info.get('DRIVER') or "pymysql"
    u = db_info.get('USER') or "root"
    pw = db_info.get('PASSWD') or "123456"
    h = db_info.get('HOST') or "localhost"
    pt = db_info.get('POST') or "3306"
    n = db_info.get('NAME') or "G_design"

    return "{}+{}://{}:{}@{}:{}/{}".format(e, d, u, pw, h, pt, n)


class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "zhangwudi2019"
    SESSION_TYPE = "redis"


class DevelopConfig(Config):
    """
    开发环境
    """
    DEBUG = True

    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "mysqlconnector",
        "USER": "root",
        "PASSWD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "G_design"
    }

    SQLALCHEMY_DATABASE_URI = get_db_info(db_info)


class TESTConfig(Config):
    """
    测试环境
    """
    TESTING = True

    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "G_design"
    }

    SQLALCHEMY_DATABASE_URI = get_db_info(db_info)


class StagingConfig(Config):
    """
    演示环境
    """
    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "G_design"
    }

    SQLALCHEMY_DATABASE_URI = get_db_info(db_info)


class ProductConfig(Config):
    """
    上线环境
    """
    db_info = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWD": "123456",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "G_design"
    }

    SQLALCHEMY_DATABASE_URI = get_db_info(db_info)


envs = {
    "develop": DevelopConfig,
    "testing": TESTConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
