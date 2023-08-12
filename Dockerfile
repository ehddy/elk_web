FROM elk_web0811

RUN apt-get update && apt-get install -y git

RUN mkdir -p /home/elk_web/

RUN git clone https://github.com/ehddy/elk_web.git /home/elk_web/

RUN mkdir -p /home/elk_web/elk/

RUN git clone https://github.com/ehddy/elk-log-analysis.git /home/elk_web/elk/


# # 환경 변수 설정
# ENV FLASK_APP=monitoring
# ENV FLASK_DEBUG=true
# ENV APP_CONFIG_FILE=/home/elk_web/config/developement.py
# 스크립트 파일에 실행 권한을 추가합니다.
RUN chmod +x /home/elk_web/start_service.sh

RUN chmod +x /home/elk_web/elk_web.sh
# /home/elk/ 디렉토리로 이동
WORKDIR /home/elk_web/



CMD ["/home/elk_web/start_service.sh"]