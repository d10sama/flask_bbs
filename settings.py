from flask_sqlalchemy import SQLAlchemy

# 数据库配置文件，输自己的就行
# db声明在这里是为了防止循环import
db = SQLAlchemy()
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '1qaz2wsx'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'javabook'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 5
