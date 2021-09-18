# 프로젝트 제목 : Finding book

### 프로젝트 설명 
도서를 검색하고 리뷰를 남기며 북마크를 저장하여 도서들을 모아볼 수 있는 사이트

### 사이트 주소
http://dromy.shop/

### Tech Stack

<table>
  
  <tr>
    <td>
      language
    </td>
    <td>
      <img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>&nbsp;
      <img src="https://img.shields.io/badge/JavaScript-F7dF1E?style=flat-square&logo=JavaScript&logoColor=white"/></a>&nbsp;
    </td>
  </tr>
  
   <tr>
    <td>
      view
    </td>
    <td>
      <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/></a>&nbsp;
      <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white"/></a>&nbsp;
    </td>
  </tr>
  
  <tr>
    <td>
      library & framework
    </td>
    <td>
      <img src="https://img.shields.io/badge/jQuery-0769AD?style=flat-square&logo=jQuery&logoColor=white"/></a>&nbsp;
      <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white"/></a>&nbsp;
    </td>
  </tr>
  
   <tr>
    <td>
      template
    </td>
    <td>
      <img src="https://img.shields.io/badge/Jinja-B41717?style=flat-square&logo=Jinja&logoColor=white"/></a>&nbsp;
    </td>
  </tr>
  
   <tr>
    <td>
      datebase
    </td>
    <td>
      <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=MongoDB&logoColor=white"/></a>&nbsp;
    </td>
  </tr>
  
   <tr>
    <td>
      deploy
    </td>
    <td>
      <img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/></a>&nbsp;
    </td>
  </tr>

</table>

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

### Database

<img src="https://user-images.githubusercontent.com/76515226/133820852-07286671-c48b-4a78-9c82-41f76ea0ddba.png"/></a>&nbsp;


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


