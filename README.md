# 프로젝트 제목 : Finding book

## 프로젝트 설명 
도서를 검색하고 리뷰를 남기며 북마크를 저장하여 도서들을 모아볼 수 있는 사이트

### API
|기능|Method|URL|
|---|---|---|
|로그인|POST|/sign_in|
|회원가입|POST|/sign_up/save|
|중복확인|POST|/sign_up/check_dup|
|마이페이지|GET|/mypage|
|도서검색|GET|/KAKAO API|
|도서 상세보기|GET|/books/read|
|리뷰 조회|GET|/reviews/read|
|리뷰 작성|POST|/reviews/new|
|북마크 저장|POST|/bookmarks/new|
|북마크 조회|GET|/bookmarks/read|
|북마크 삭제|POST|/bookmarks/delete|
