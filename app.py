from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import markdown
load_dotenv()

app = Flask(__name__)

def send_email(content):
    # 이메일 설정
    sender_email = os.getenv('EMAIL_USER')  # .env 파일에서 이메일 주소 가져오기
    sender_password = os.getenv('EMAIL_PASSWORD')  # .env 파일에서 이메일 비밀번호 가져오기
    receiver_email = os.getenv('RECEIVER_EMAIL')  # .env 파일에서 수신자 이메일 주소 가져오기
    
    # 이메일 메시지 생성
    message = MIMEMultipart('alternative')
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = f'{datetime.now().strftime("%Y-%m-%d")} GPT-4o-mini의 기술 뉴스 업데이트'
    
    # 마크다운을 HTML로 변환
    html_content = markdown.markdown(content)
    
    # HTML 스타일 추가
    styled_html = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-family: monospace;
                }}
                pre {{
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 0;
                    padding-left: 15px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
    </html>
    """
    
    # HTML 형식의 이메일 본문 추가
    message.attach(MIMEText(styled_html, 'html'))
    
    try:
        # Gmail SMTP 서버 연결
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # 이메일 전송
        server.send_message(message)
        server.quit()
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {str(e)}")

def scheduled_job():
    try:
        print(f"스케줄된 작업 시작: {datetime.now()}")
        gpt4o_mini = ChatOpenAI(
            model_name="gpt-4o-mini",
            temperature=0.7,
        )
        tool = TavilySearchResults()
        tools = [tool]
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are a helpful AI assistant that provides daily blockchain, AI and security tech news and updates. 
            Search for the latest technology news and provide a concise summary of the most important developments.
             Please find and provide news or information that has occurred within the last 3 days.
             today is {datetime.now().strftime('%Y-%m-%d')}.
             please answer in korean.
             """),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_tools_agent(gpt4o_mini, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        print("^^^")
        result = agent_executor.invoke({
            "input": f"최근 블록체인, AI 및 보안 기술 뉴스를 제공해주세요. 오늘은 {datetime.now().strftime('%Y-%m-%d')}입니다."
        })
        
        # 결과를 이메일로 전송
        if 'output' in result:
            send_email(result['output'])
        
        print(result)
        print("vvv")
        print(f"스케줄된 작업 완료: {datetime.now()}")
    except Exception as e:
        print(f"스케줄된 작업 실행 중 오류 발생: {str(e)}")
        # 여기에 에러 알림 로직을 추가할 수 있습니다 (예: 이메일 알림)

if __name__ == "__main__":
    try:
        scheduler = BackgroundScheduler(timezone='Asia/Seoul')
        scheduler.add_job(scheduled_job, 'cron', hour=6, minute=30, second=0, misfire_grace_time=60, timezone='Asia/Seoul')
        scheduler.start()
        print("스케줄러가 시작되었습니다.")
        
        # Flask 애플리케이션 실행
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {str(e)}")
    finally:
        scheduler.shutdown()
        print("스케줄러가 종료되었습니다.")

# flask run --no-reload