from settings import db


# model中一个类就是一个表，ORM模式
class User(db.Model):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.level = 1
        self.coin = 5

    __tablename__ = 'user'

    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    coin = db.Column(db.Integer, nullable=False)
    introduction = db.Column(db.String(200))

    def __repr__(self):
        return '<User %r>' % self.username

    # serialize用于输出json串
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class Article(db.Model):
    def __init__(self, author_id, title, content, html):
        self.author_id = author_id
        self.title = title
        self.content = content
        self.html = html

    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Text)
    content = db.Column(db.Text)
    html = db.Column(db.Text)
    author_id = db.Column(db.String(10), db.ForeignKey('user.id'))

    def serialize(self):
        return {
            'id': self.id,
            'author_id': self.author_id,
            'title': self.title,
            'content': self.content,
            'html': self.html
        }

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Resource(db.Model):

    def __init__(self, id, title, type, info, cost, path):
        self.a_id = id
        self.title = title
        self.type = type
        self.info = info
        self.cost = cost
        self.path = path

    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.String(10), db.ForeignKey(User.id))
    title = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(50))
    info = db.Column(db.String(200))
    cost = db.Column(db.Integer)
    path = db.Column(db.VARCHAR(256))

    def serialize(self):
        return {
            'title': self.title,
            'type': self.type,
            'info': self.info,
            'cost': self.cost,
            'path': self.path,
            'id': self.id
        }


class Admin(db.Model):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    __tablename__ = 'admin'
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(16), nullable=False)

    # 重写print和str的方法
    def __repr__(self):
        return '<Admin %r>' % self.username

    # serialize用于输出json串
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }


class Pinned(db.Model):
    def __init__(self, id, uid, aid):
        self.id = id
        self.uid = uid
        self.aid = aid

    __tablename__ = 'pinned'
    id = db.Column(db.Integer, primary_key=True, )
    uid = db.Column(db.String(10))
    aid = db.Column(db.Integer)

    # 重写print和str的方法
    def __repr__(self):
        return '<Pinned %r>' % self.id

    # serialize用于输出json串
    def serialize(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'aid': self.aid
        }


class Report(db.Model):
    def __init__(self, user_id, user_name, gender, aff, mob, dom, status):
        self.user_id = user_id
        self.user_name = user_name
        self.gender = gender
        self.aff = aff
        self.mob = mob
        self.dom = dom
        self.status = status

    __tablename__ = 'Report'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(16))
    gender = db.Column(db.Integer)
    aff = db.Column(db.String(10))
    mob = db.Column(db.String(12))
    dom = db.Column(db.String(10))
    status = db.Column(db.String(30))

    # 重写print和str的方法
    def __repr__(self):
        return '<Report %r>' % self.user_id

    # serialize用于输出json串
    def serialize(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'gender': self.gender,
            'aff': self.aff,
            'mob': self.mob,
            'dom': self.dom,
            'status': self.status
        }


class rep_info(db.Model):
    def __init__(self, report_id, user_id, hasComplete):
        self.report_id = report_id
        self.user_id = user_id
        self.hasComplete = hasComplete

    __tablename__ = 'rep_info'
    report_id = db.Column(db.String(16), primary_key=True)
    user_id = db.Column(db.String(16))
    hasComplete = db.Column(db.Integer)

    # 重写print和str的方法
    def __repr__(self):
        return '<rep_info %r>' % self.report_id

    # serialize用于输出json串
    def serialize(self):
        return {
            'report_id': self.report_id,
            'user_id': self.user_id,
            'hasComplete': self.hasComplete
        }
