# user模块
import json
import os
import string

from sqlalchemy.future import engine

from user import user_blueprint
from models import User, db, Article, Resource, Pinned, Report, Admin, rep_info
from flask import request, Response, jsonify, send_from_directory, make_response
from sqlalchemy import or_,and_

presentuser = ''


@user_blueprint.route('/register', methods=['post'])
def register():
    data = request.get_json()
    user_id = data['id']
    global presentuser
    presentuser = user_id
    username = data['username']
    password = data['password']
    user = User(user_id, username, password)
    db.session.add(user)
    db.session.commit()
    return 'success'


@user_blueprint.route('/register_a', methods=['post'])
def register_a():
    data = request.get_json()
    user_id = data['id']
    global presentuser
    presentuser = user_id
    username = data['username']
    password = data['password']
    user = Admin(user_id, username, password)
    db.session.add(user)
    db.session.commit()
    return 'success'


@user_blueprint.route('/login', methods=['post'])
def login():
    data = request.get_json()
    user_id = data['id']
    password = data['password']
    record1 = Admin.query.get(user_id)
    record2 = User.query.get(user_id)
    global presentuser
    presentuser = user_id
    if record1:
        if record1.password == password:
            print('welcome ' + record1.username)
            response = {'res': 'success_a'}
            return response
        else:
            response = {'res': 'failed'}
            return response
    if record2:
        if record2.password == password:
            print('welcome ' + record2.username)
            response = {'res': 'success'}
            return response
        else:
            response = {'res': 'failed'}
            return response
    response = {'res': 'failed'}
    return response


@user_blueprint.route('/edit', methods=['post'])
def edit():
    data = request.get_json()
    id = data['id']
    username = data['username']
    introdcution = data['introduction']
    User.query.filter(User.id == id).update({'username': username})
    User.query.filter(User.id == id).update({'introduction': introdcution})
    response = {'res': 'success', 'username': username, 'introduction': introdcution}
    return response


@user_blueprint.route('/getInfo', methods=['post'])
def getInfo():
    data = request.get_json()
    id = data['id']
    user = User.query.filter(User.id == id).first()

    if user:
        response = {'res': 'success', 'username': user.username, 'introduction': user.introduction}
        return response
    else:
        response = {'res': 'failed'}
        return response


@user_blueprint.route('/savemd', methods=['post'])
def save_md():
    data = request.get_json()
    id = data['id']
    title = data['title']
    type = data['type']
    content = data['content']
    html = data['html']
    article = Article(id, title, content, html)
    db.session.add(article)
    db.session.commit()
    response = {'res': 'success', 'html': html}
    return response


@user_blueprint.route('/getArticleList', methods=['post'])
def getalist():
    data = request.get_json()
    id = data['id']
    alist = Article.query.filter(Article.author_id == id).all()
    response = {'res': 'success', 'alist': json.dumps([row.serialize() for row in alist])}
    print(response)
    return response


@user_blueprint.route('/getResourceList', methods=['post'])
def getrlist():
    data = request.get_json()
    id = data['id']
    rlist = Resource.query.filter(Resource.a_id == id).all()
    response = {'res': 'success', 'rlist': json.dumps([row.serialize() for row in rlist])}
    return response


@user_blueprint.route('/article', methods=['post'])
def article():
    data = request.get_json()
    print(data)
    a_id = data['a_id']
    article = Article.query.filter(Article.id == a_id).first()
    response = {'res': 'success', 'article': article.serialize()}
    print(response)
    return response


@user_blueprint.route('/resource', methods=['post'])
def resource():
    data = request.get_json()
    print(data)
    r_id = data['r_id']
    resource = Resource.query.filter(Resource.id == r_id).first()
    response = {'res': 'success', 'resource': resource.serialize()}
    return response


@user_blueprint.route('/upload', methods=["post"])
def upload():
    # files = request.files  # Flask中获取文件
    files = request.files
    file_obj = files['file']
    f_name = file_obj.filename
    if file_obj is None:
        # 表示没有发送文件
        response = {'res': 'failed'}
        return response
    # 保存文件
    file_dir = os.path.join(os.getcwd(), 'files')
    file_path = os.path.join(file_dir, f_name)
    duplicate = 0
    while os.path.exists(file_path):
        name = f_name.split('.')
        dupname = name[0].split('_')
        name[0] = dupname[0] + "_" + str(duplicate)
        f_name = name[0] + "." + name[1]
        file_path = os.path.join(file_dir, f_name)
        duplicate += 1
    file_path = os.path.join(file_dir, f_name)
    file_obj.save(file_path)
    if duplicate != 0:
        response = {'res': 'success', 'duplicate': duplicate}
    else:
        response = {'res': 'success', 'duplicate': ''}
    return response


@user_blueprint.route('/record', methods=['post'])
def record():
    data = request.get_json()
    print(data)
    id = data['id']
    title = data['title']
    cost = data['cost']
    type = data['type']
    desc = data['desc']
    filename = data['filename']
    duplicate = data['duplicate']
    f_name = filename.split('.')
    if duplicate != '':
        filename = f_name[0] + "_" + str(duplicate - 1) + "." + f_name[1]
    else:
        filename = f_name[0] + "." + f_name[1]
    file_dir = os.path.join(os.getcwd(), 'files')
    file_path = os.path.join(file_dir, filename)
    record = Resource(id, title, type, desc, cost, file_path)
    db.session.add(record)
    db.session.commit

    response = {'res': 'success'}
    return response


@user_blueprint.route('/search_a', methods=['POST'])
def receive_data_and_query():
    data = request.get_json()
    print(data)
    content = data['tosearch']
    content = '%' + content + '%'
    result1 = db.session.query(Article).filter(
        or_(Article.title.like(content), Article.content.like(content))).order_by(Article.id).all()
    result2 = db.session.query(User.id).filter(User.username.like(content))
    result = db.session.query(Article).filter(Article.author_id.in_(result2)).order_by(Article.id).all()
    result += result1
    if len(result) > 0:
        res = {'res': 'success', 'article': json.dumps([row.serialize() for row in result])}
        return res
    else:
        res = {'res': 'failed'}
        return res


@user_blueprint.route('/search_r', methods=['POST'])
def receive_data_and_query_r():
    data = request.get_json()
    print(data)
    content = data['tosearch']
    content = '%' + content + '%'
    result = db.session.query(Resource).filter(
        or_(Resource.title.like(content), Resource.type.like(content), Resource.a_id.like(content))).order_by(
        Resource.id).all()

    if len(result) > 0:
        res = {'res': 'success', 'resource': json.dumps([row.serialize() for row in result])}
        return res
    else:
        res = {'res': 'failed'}
        return res


@user_blueprint.route('/getResource', methods=['GET', 'POST'])
def download():
    data = request.get_json()
    print(data)
    content = data['path']
    pin = data['pin']
    if pin == '':
        file_dir = content.split('\\')
        fname = file_dir[len(file_dir) - 1]
        file_dir = file_dir[:len(file_dir) - 1]
        fd = ''
        count = 0
        for x in file_dir:
            if count < len(file_dir) - 1:
                fd += x + '\\'
                count += 1
            else:
                fd += x
        response = make_response(send_from_directory(fd, fname, as_attachment=True))
        print("response: ", response)
        response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
        print("response: ", response.headers)
        return response
    else:
        uid = presentuser
        size = db.session.query(Pinned).all()
        pinned = Pinned(len(size), str(pin), int(uid))
        db.session.add(pinned)
        res = {'res': 'success'}
        return res


@user_blueprint.route('pinnedArticle', methods=['POST'])
def pinndArticle():
    data = request.get_json()
    content = data['id']
    result1 = db.session.query(Resource).filter(Resource.a_id == content).order_by(Resource.id).all()
    response = {'rlist': json.dumps([row.serialize() for row in result1])}

    return response


@user_blueprint.route('searchstuinfo', methods=['POST'])
def getStuinfo():
    # 空数据不用管
    data = request.get_json()
    sid = data['stu_id']
    sn = data['stu_name']
    aff = data['aff']
    dom = data['dom']
    mob = data['mob']
    status = data['status']
    # print(sid+" "+sn+" "+aff+" "+dom+" "+mob+" "+status)
    result = db.session.query(Report).filter(
        or_(Report.user_id == sid, Report.user_name == sn, Report.aff == aff, Report.dom == dom, Report.mob == mob,
            Report.status == status)).order_by(Report.user_id).all()
    response = {'res': json.dumps([row.serialize() for row in result])}
    print(response)
    return response


@user_blueprint.route('isRep', methods=['POST'])
def isRep():
    # 空数据不用管
    data = request.get_json()
    sid = data['stu_id']
    result = db.session.query(rep_info).filter(and_(rep_info.user_id == sid, rep_info.hasComplete == 1)).order_by(rep_info.user_id).all()
    print(len(result))
    if len(result) < 1:
        response = {'success': '0'}
    else:
        response = {'success': '1'}
    return response


@user_blueprint.route('totalDangerousNum', methods=['POST'])
def totalDangerousNum():
    # 空数据不用管
    response = {'success': '114514'}
    return response
