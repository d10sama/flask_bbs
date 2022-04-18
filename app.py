from flask import Flask, render_template, request, redirect, url_for
from flask import request
from flask_cors import CORS

from admin import admin_blueprint
from user import user_blueprint
from models import User, Admin
from settings import db

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(user_blueprint, url_prefix='/user')


def create():
    with app.app_context():
        db.create_all()
        return True
    return false


# 这是路由，暂时还没研究分级路由，先写在一起吧
# 写的时候可以把路由下的函数分离开来写成单个文件
@app.route('/')
def index():
    if create():
        return 'fk my life'
    else:
        return 'error'


if __name__ == '__main__':
    app.run(debug=True)


