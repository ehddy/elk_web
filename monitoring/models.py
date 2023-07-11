from monitoring import db

"""
server_default를 사용하면 flask db upgrade 명령을 수행할 때 
해당 속성을 갖고 있지 않던 기존 데이터에도 기본값이 저장된다. 
하지만 default는 새로 생성되는 데이터에만 기본값을 생성해 준다. 
따라서 현재처럼 "없던 속성을 만들어야 하는 상황"에서는 default 대신 server_default를 사용
"""

"""
오류 내용 : 어떤 모델에 nullable=Flase 인 속성을 추가하고자 할 때 기존에 이미 저장되어 있던 데이터 떄문에 발생한 오류 
해결법 : 
user_id의 nullable 설정을 False 대신 True로 바꾸기
user_id를 임의의 값으로 설정하기(여기서는 1로 설정 (, nullable=True, 
server_default='1'))
flask db migrate 명령, flask db upgrade 명령 다시 실행하기
user_id의 nullable 설정을 다시 False로 변경하기
flask db migrate 명령, flask db upgrade 명령 다시 실행하기
""" 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


