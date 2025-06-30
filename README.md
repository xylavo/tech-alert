# Tech Alert

AI 기반 기술 뉴스 자동 알림 서비스

## 소개
이 프로젝트는 매일 아침 최신 블록체인, AI, 보안 기술 뉴스를 요약하여 이메일로 자동 발송하는 Python 애플리케이션입니다. OpenAI의 GPT-4o-mini와 Tavily Search를 활용하여 3일 이내의 주요 기술 뉴스를 수집하고, 결과를 마크다운 및 HTML로 변환해 이메일로 전송합니다.

## 주요 기능
- 매일 오전 6시 30분(Asia/Seoul) 자동 뉴스 수집 및 이메일 발송
- 블록체인, AI, 보안 분야의 최신 뉴스 요약
- 결과를 마크다운 및 HTML로 변환하여 가독성 높은 이메일 제공
- Flask 서버 구동(기본 포트: 5000)

## 설치 방법
1. 저장소 클론 및 디렉토리 이동
```bash
git clone <저장소_URL>
cd tech-alert
```
2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

## 환경 변수 설정
`.env` 파일에 아래 항목을 추가하세요:
```
EMAIL_USER=발신자_이메일주소
EMAIL_PASSWORD=이메일_앱_비밀번호
RECEIVER_EMAIL=수신자_이메일주소
OPENAI_API_KEY=OpenAI_API_키
TAVILY_API_KEY=Tavily_API_키
```

## 실행 방법
```bash
python app.py
```

## 주요 의존성
- Flask
- APScheduler
- python-dotenv
- langchain
- openai
- tavily-search
- markdown

## 동작 방식
1. 스케줄러가 매일 오전 6시 30분에 `scheduled_job` 함수 실행
2. GPT-4o-mini와 Tavily Search로 최신 기술 뉴스 검색 및 요약
3. 결과를 마크다운 → HTML로 변환 후 이메일 발송
4. Flask 서버는 0.0.0.0:5000에서 실행(기본값)

## 참고 사항
- Gmail 등 SMTP를 사용할 경우, 앱 비밀번호를 발급받아야 할 수 있습니다.
- OpenAI, Tavily API 키가 필요합니다.
- 뉴스 요약 결과는 한국어로 제공됩니다.

## 라이선스
MIT 