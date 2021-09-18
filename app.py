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

client = MongoClient('mongodb://13.209.82.68', 27017, username="test", password="test")
# client = MongoClient('mongodb://test:test@localhost', 27017,)
db = client.dbsparta_findingbook


# 메인페이지 렌더링
@app.route('/')
def home():
    # mytoken 이라는 cookie를 가져온다.
    token_receive = request.cookies.get('mytoken')
    # 로그인 인증 예외처리
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return render_template('index.html', user_exist=bool(payload['id'])) # view 처리때문에 login 여부 넘거줌
    except jwt.ExpiredSignatureError:      # jwt 생성시 payload에 기입한 로그인 만료시간이 지나면 발생
        # return redirect(url_for("/", msg="로그인 시간이 만료되었습니다."))
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        # return redirect(url_for("/", msg="로그인 정보가 존재하지 않습니다."))
        return render_template('index.html', msg="로그인 정보가 존재하지 않습니다.")

# 로그인 페이지 열기
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

# 로그인 기능
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 클라이언트로부터 id,pw 받아옴
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest() # 패스워드 해시라이브러리를 이용해 인코딩
    result = db.users.find_one({'username': username_receive, 'password': pw_hash}) # db에서 정보 찾기

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') # jwt 토큰 발행

        return jsonify({'result': 'success', 'token': token}) # json 형식으로 return
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

#회원가입
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest() # 클라이언트에서 받아온 password 값을 인코딩
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
    exists = bool(db.users.find_one({"username": username_receive})) # db에 id 검색
    return jsonify({'result': 'success', 'exists': exists})          # id 유무 return


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
@app.route('/books/read')
def book_detail():
   isbn = request.args.get('isbn') # 도서번호
   token_receive = request.cookies.get('mytoken') # 쿠키에서 mytoken jwt를 받아옴
   if token_receive is not None: # 로그인 상태 체크
       payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
       id=payload['id']
       heart_count = db.bookmark.find({'username': id, 'isbn': isbn}).count() # 하트 이미지 변경을 위해 해당 id의 해당 도서 북마크 개수 조회
       return render_template('detail.html', isbn=isbn, user_exist=bool(payload['id']), heart_stat = heart_count) # python to javascript는 bool 타입을 못읽어서 int로 return
   else:
       return render_template('detail.html', isbn=isbn, heart_stat = 0)

# 리뷰 작성
@app.route('/reviews/new', methods=['POST'])
def make_review():
    token_receive = request.cookies.get('mytoken') # 쿠키에서 mytoken jwt를 받아옴
    if token_receive is None: # mytoken jwt가 없을때
        return jsonify({'msg': '로그인을 먼저 해주세요'})
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload['id']                      # id
        review = request.form['review_give']    # review 내용
        isbn = request.form['isbn_give']        # 도서번호
        regdate = request.form['regdate']       # 등록시간

        doc = {
            'username': id,
            'review': review,
            'isbn': isbn,
            'regdate': regdate
        }

        db.reviews.insert_one(doc)    # review 정보 insert

        return jsonify({'msg': '리뷰 작성 성공!'})

# 리뷰 조회
@app.route('/reviews/read', methods=['GET'])
def read_review():
   isbn = request.args.get('isbn')  # 도서번호
   reviews = list(db.reviews.find({'isbn': isbn}))  # db에 도서번호 조회
   return jsonify({'reviews': dumps(reviews)})  # 해당 도서번호 review 정보 return

# 북마크 저장
@app.route('/bookmarks/new', methods=['POST'])
def bookmark():
    token_receive = request.cookies.get('mytoken')  # 쿠키에서 mytoken jwt를 받아옴
    if token_receive is None:       # mytoken jwt가 없을때
        return jsonify({'msg': '로그인을 먼저 해주세요'})
    else:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        id = payload['id']                          # id
        isbn = request.form['isbn']                 # 도서번호
        title = request.form['title']               # 책 제목
        thumbnail = request.form['thumbnail']       # 썸네일 이미지

        count = db.bookmark.find({'username': id, 'isbn': isbn}).count()  # 해당 사용자의 해당 도서의 북마크 정보의 개수 조회
        if count > 0:
            return jsonify({'msg': '이미 북마크한 도서입니다'})
        else:
            doc = {
                'username': id,
                'isbn': isbn,
                'title': title,
                'thumbnail': thumbnail
            }

            db.bookmark.insert_one(doc) # db에 bookmark 저장

            return jsonify({'msg': '북마크 저장 완료!'})

# 마이페이지
@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

# 북마크 조회
@app.route('/bookmarks/read')
def show_bookmark():   # 로그인 회원만 북마크버튼이 보이기때문에 북마크에선 따로 로그인예외처리 안함
    token_receive = request.cookies.get('mytoken')  # 쿠키에서 mytoken jwt를 받아옴
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    id = payload['id']

    bookmarks = db.bookmark.find({'username': id}, {'_id': False})  # db에서 해당 id의 북마크된 도서정보 조회
    bookmarks_count = db.bookmark.find({'username': id}, {'_id': False}).count() # db에서 해당 id의 북마크된 도서정보 개수 조회

    return jsonify({'bookmarks': dumps(bookmarks), 'bookmarks_count':bookmarks_count}) # 북바크 도서정보, 도서개수 json형식 return

# 북마크 삭제
@app.route('/bookmarks/delete', methods=['POST'])
def delete_bookmark():
    token_receive = request.cookies.get('mytoken')  # 쿠키에서 mytoken jwt를 받아옴
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    num_receive = int(request.form['number_give']) # 지우려는 책의 index (request.form[] 으로는 str 데이터로 값을 받아와서 int로 파싱)
    id = payload['id']
    isbn = list(db.bookmark.find({'username': id}))[num_receive]['isbn'] # 지우려는 책의 도서번호
    print(isbn)

    db.bookmark.delete_one({'username': id, 'isbn': isbn}) # 해당 도서 삭제

    return jsonify({'msg': '북마크 삭제 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)