from flask import Blueprint, url_for, render_template, flash, request, session, g, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify  # jsonify 함수를 임포트해야 합니다
from werkzeug.utils import redirect
from monitoring.views.auth_views import login_required
from io import BytesIO
from datetime import datetime, timedelta
from monitoring.forms import UserSearchId
# from elk.segment import * 
# from pybo.models import Question
from elk.elk_program import *

import openpyxl
import pytz

bp = Blueprint('manage', __name__, url_prefix='/manage')


@bp.route('/show_abnormal_user/')   
@login_required
def show_abnormal():
    e = Elk()
    try:
        data = e.get_abnormal_data_show()
    except:
        data = pd.DataFrame(data={}, columns=['가입자 ID', '비정상 판별 횟수','판별 등급', '판별 요인', '평균 접속 수(1분)', '차단율(%)','최다 접속 URL', '최다 접속 IP 위치', '접속 기간'])

    return render_template('abnormal_describe.html', data=data)

@bp.route('/delete_rows', methods=['POST']) # 경로를 '/delete_rows'가 아닌 '/manage/delete_rows'로 수정
@login_required
def delete_rows():
    name_list = request.json  

    e = Elk()

    for name in name_list:
        e.delete_data_by_id('abnormal_describe*', name)

    return jsonify({'message': '삭제'}), 200



    