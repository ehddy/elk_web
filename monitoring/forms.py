from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserLoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired("사용자명은 필수입력 항목입니다."), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired("비밀번호는 필수입력 항목입니다.")])
    

class UserSearchId(FlaskForm):
    userid = StringField('User ID', validators=[DataRequired("사용자 ID은 필수입력 항목입니다."), Length(min=3, max=25)])

