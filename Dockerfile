FROM elk_web0811

COPY ./ /home/elk_web/


# 스크립트 파일에 실행 권한을 추가합니다.
RUN chmod +x /home/elk_web/start_service.sh

CMD ["/home/elk_web/start_service.sh"]