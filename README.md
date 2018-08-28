# kulhouse_stayout
건국대학교 서울캠퍼스 기숙사 쿨하우스 자동 주말 외박 신청 프로그램.  
본 프로그램은 python 3.6 기준으로 작성되었습니다.
 
* * *   

## 사용방법  
1. config.ini 수정  
    1) client_stdnum에 본인의 학번을 적어주세요.  
        Example) client_stdnum = 201711111  
    2) client_password에 쿨하우스 웹페이지에 해당 학번으로 등록된 등록된 비밀번호를 적어주세요.  
        Example) client_password = 1q2w3e4r
        
    * 만약 비밀번호가 없다면 [KULHOUSE](https://kulhouse.konkuk.ac.kr/home/login/find_pop.asp)에서 비밀번호를 설정해주세요.

2. stayout.py를 실행시켜주세요  
    `python stayout.py`

* * *
사용한 외부 라이브러리는 다음과 같습니다.  

* aiohttp
* BeautifulSoup
