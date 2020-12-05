# README

해당 코딩은 웹에서 이미지를 크롤링해주는 코드입니다.

1. 크롤링을 하기 위해 우선 [chromedriver](http://blog.naver.com/PostView.nhn?blogId=jinpw&logNo=221572005266)을 다운받아야합니다. 
   * chromedriver란 크롬 브라우저를 자동적으로 테스트하는 툴입니다. 크롤링할때 필수적이기 때문에 꼭 다운 받습니다. 
   * 다운 받고 경로를 꼭 기억합시다!
   * 그리고 `executable_path`에 chromedriver의 경로를 지정해줍니다.
2. 크롤링 하는데 필요한 두가지 라이브러리를 install 합시다
   * pip install beautifulsoup4
   * pip install selenium
3. 입력의 경우 한글명과 영어명으로 이루어져있고, 한글명은 bing.com에 검색해주는 단어이고, 영어명은 images폴더 내에 저장시킬 이름 입니다.
   * ex) 한글명 : 호랑이, 영어명: tiger 이렇게 하시면 됩니다.
   * 만약에 한번에 여러 동물을 하고싶을경우
   * 한글명 : 호랑이 사자, 영어명 : tiger lion 이렇게 순서대로 띄어쓰기 하시면 됩니다.
4. 코드 43줄 보시면, cnt 1회당 약 50~60개의 이미지를 추출하니까 참고하시기 바랍니다.
5. 이미지를 크롤링하다가 더이상 추출할 이미지가 없을경우 자동으로 프로그램은 종료됩니다.

