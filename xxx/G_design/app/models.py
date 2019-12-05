from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    # 暂定三个权限（0，1，2），实际是两个，0为未激活
    role = db.Column(db.Integer, nullable=False, default=0)
    user = db.Column(db.String(16), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)

    # 加上property装饰器后，会把函数变为属性，属性名即为函数名
    @property
    def password(self):
        """读取属性的函数行为"""
        # print(user.password)  # 读取属性时被调用
        # 函数的返回值会作为属性值
        # return "xxxx"
        raise AttributeError("这个属性只能设置，不能读取")

    # 使用这个装饰器, 对应设置属性操作
    @password.setter
    def password(self, value):
        """
        设置属性  user.passord = "xxxxx"
        :param value: 设置属性时的数据 value就是"xxxxx", 原始的明文密码
        :return:
        """
        self.password_hash = generate_password_hash(value)

    # def generate_password_hash(self, origin_password):
    #     """对密码进行加密"""
    #     self.password_hash = generate_password_hash(origin_password)

    def check_password(self, passwd):
        """
        检验密码的正确性
        :param passwd:  用户登录时填写的原始密码
        :return: 如果正确，返回True， 否则返回False
        """
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        user_dict = {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'user': self.user,
        }

        return user_dict
