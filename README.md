# 프로젝트 제목 : Finding book

## 프로젝트 설명 
도서를 검색하고 리뷰를 남기며 북마크를 저장하여 도서들을 모아볼 수 있는 사이트

### 와이어프레임

1. 메인페이지
  - 검색창에 키워드를 검색하면 해당 키워드를 포함한 제목을 가진 책을 검색
<img src="https://user-images.githubusercontent.com/51510602/133717933-ce551b01-117f-4478-a0e3-c30d6aa4d7e6.png" width="400" height="400"/>

2. 로그인/회원가입 페이지(팝업)
  - 로그인 페이지를 팝업으로 띄움
<img src="https://user-images.githubusercontent.com/51510602/133717958-93aa4ca5-7a99-447a-a953-c7d3899c568f.png" width="400" height="400"/>

<img src="https://user-images.githubusercontent.com/51510602/133717974-f02675ff-994c-40de-a174-0808f60357f2.png" width="400" height="400"/>

3. 책 상세페이지
  - 메인페이지에서 책을 클릭하면 상세페이지로 넘어와 책의 상세정보를 보여줌
  - 리뷰작성
<img src="https://user-images.githubusercontent.com/51510602/133717980-2861d9a3-0e20-4550-8679-1c90c41f27f6.png" width="400" height="400"/>

4. 마이페이지
  - 상세페이지에서 찜 버튼을 누르면 마이페이지에 책 저장
<img src="https://user-images.githubusercontent.com/51510602/133717993-d03ac5ba-2167-4d9a-b8b5-e8a7c65063d6.png" width="400" height="400"/>

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
