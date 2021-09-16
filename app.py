from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from bson.json_util import dumps

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'

client = MongoClient('mongodb://3.36.68.250', 27017, username="test", password="test")
db = client.dbsparta_plus_week4


@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', user_exist=bool(payload['id']))
    except jwt.ExpiredSignatureError:
        # return redirect(url_for("/", msg="로그인 시간이 만료되었습니다."))
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        # return redirect(url_for("/", msg="로그인 정보가 존재하지 않습니다."))
        return render_template('index.html', msg="로그인 정보가 존재하지 않습니다.")


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/user/<username>')
def user(username):
    # 각 사용자의 프로필과 글을 모아볼 수 있는 공간
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (username == payload["id"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"username": username}, {"_id": False})
        return render_template('user.html', user_info=user_info, status=status)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')#.decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

#회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})

# 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


@app.route('/update_profile', methods=['POST'])
def save_img():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 프로필 업데이트
        return jsonify({"result": "success", 'msg': '프로필을 업데이트했습니다.'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route('/posting', methods=['POST'])
def posting():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅하기
        return jsonify({"result": "success", 'msg': '포스팅 성공'})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@app.route("/get_posts", methods=['GET'])
def get_posts():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 포스팅 목록 받아오기
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다."})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

# 도서 상세보기 페이지
@app.route('/detail')
def book_detail():
   isbn = request.args.get('isbn')
   # print(isbn)
   return render_template('detail.html', isbn=isbn)

# 리뷰 작성
@app.route('/review', methods=['POST'])
def make_review():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return jsonify({'msg': '로그인을 먼저 해주세요'})
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload['id']
        review = request.form['review_give']
        isbn = request.form['isbn_give']

        doc = {
            'username': id,
            'review': review,
            'isbn': isbn
        }

        db.reviews.insert_one(doc)

        return jsonify({'msg': '리뷰 작성 성공!'})

# 리뷰 조회
@app.route('/review', methods=['GET'])
def read_review():
   isbn = request.args.get('isbn')
   reviews = list(db.reviews.find({'isbn': isbn}))
   # print(isbn, len(reviews))
   return jsonify({'reviews': dumps(reviews)})

# 북마크 저장
@app.route('/bookmark', methods=['POST'])
def bookmark():
    token_receive = request.cookies.get('mytoken')
    if token_receive is None:
        return jsonify({'msg': '로그인을 먼저 해주세요'})
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload['id']
        isbn = request.form['isbn']
        title = request.form['title']
        thumbnail = request.form['thumbnail']

        count = db.bookmark.find({'username': id, 'isbn': isbn}).count()
        # print(count)
        if count > 0:
            return jsonify({'msg': '이미 북마크한 도서입니다'})
        else:
            doc = {
                'username': id,
                'isbn' : isbn,
                'title': title,
                'thumbnail': thumbnail
            }

            db.bookmark.insert_one(doc)

            return jsonify({'msg': '북마크 저장 완료!'})

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

# 북마크 조회
@app.route('/mybook')
def show_bookmark():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    id = payload['id']

    bookmarks = db.bookmark.find({'username': id}, {'_id':False})
    # print(bookmark)

    # return render_template('mypage.html', bookmark=dumps(bookmarks))
    # return render_template('mypage.html', bookmark=bookmarks)
    return jsonify({'bookmarks': dumps(bookmarks)})

# 북마크 삭제
@app.route('/mybook/delete', methods=['POST'])
def delete_bookmark():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    id = payload['id']
    isbn = request.form['isbn']
    print(isbn)

    db.bookmark.delete_one({'username': id, 'isbn': isbn})

    return jsonify({'msg': '북마크 삭제 완료!'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)