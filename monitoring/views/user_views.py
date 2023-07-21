from flask import Blueprint, url_for, render_template, flash, request, session, g, Response
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import redirect
from monitoring.views.auth_views import login_required
from io import BytesIO
from datetime import datetime, timedelta
from monitoring.forms import UserSearchId
# from elk.segment import * 
# from pybo.models import Question
from elk.elk_program import *
from elk.visualize import *
import openpyxl
# main_views가 인수로 전달, 첫 번째 인수 main은 블루프린트의 별칭
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/mainboard/')
@login_required
def mainboard():
    return render_template('mainboard.html')


@bp.route('/abnormaly_board/')
@login_required
def abnormaly_board():
    return render_template('abnormaly_user_board.html')
    


@bp.route('/search/', methods=('GET', 'POST'))
@login_required
def user_dashboard():
    form = UserSearchId()
    graphJSON = False
    if request.method == "POST" and form.validate_on_submit():
        error = None
        userid = form.userid.data
        e = Elk()
        v = Visualize()
        # try:
        data = e.get_sDevID_data(userid)
        scaled_data = e.preprocessing_data(data)
        describe_data = e.describe(scaled_data)

        fig_gage = v.get_dash_gage(describe_data)
        fig_ip_host = v.get_dash_ipchart(scaled_data)
        fig_seasonal = v.get_dash_seasonal(scaled_data)
        fig_ua_port  = v.get_dash_ua_port(scaled_data)

        graph_gage = fig_gage.to_json()
        graph_ip_host = fig_ip_host.to_json()
        graph_seasonal = fig_seasonal.to_json()
        graph_ua_port = fig_ua_port.to_json()
        
        
        # except:
        #     error = "No exist User Id or logs"
        #     flash(error)
       
        return render_template('user_dashboard.html',  form=form, graph_gage=graph_gage, graph_ip_host=graph_ip_host, graph_seasonal=graph_seasonal, graph_ua_port=graph_ua_port)

    return render_template('user_dashboard.html', form=form, graphJSON=graphJSON)


@bp.route('/user_describe/', methods=('GET', 'POST'))
@login_required
def user_describe():
    form = UserSearchId()
    data_return = False
    df1 = False 
    df2 = False
    ip_describe_data = False
    if request.method == "POST" and form.validate_on_submit():
        error = None
        userid = form.userid.data

        e = Elk()

        try:
            data = e.get_sDevID_data(userid)
            scaled_data = e.preprocessing_data(data)
            ip_describe_data  = e.get_ip_describe(scaled_data)

            ip_describe_data.rename({'sHost': '접속 주소', 'uDstIp':'IP 주소', 'sUA': '유저 에이전트', 'connect_count': '접속 수', 'country':'국가', 'regionName':'지역', 'city':'도시'}, axis=1, inplace=True)
            describe_data = e.describe(scaled_data)
            split_column = len(describe_data.columns) // 2
            df1 = describe_data.iloc[:, :split_column]
            df2 = describe_data.iloc[:, split_column:]
            data_return = True
        except:
            error = "No exist User Id or logs"
            flash(error)
       
        return render_template('user_describe.html', form=form, describe_data1=df1, describe_data2=df2,data_return=data_return, ip_data=ip_describe_data)


    return render_template('user_describe.html', form=form, data_return=data_return)


@bp.route('/search_user_data/', methods=('GET', 'POST'))
@login_required
def user_data():
    form = UserSearchId()
    scaled_data = None
    data_return = False
    data = None
    if request.method == "POST" and form.validate_on_submit():
        error = None
        
        userid = form.userid.data


        e = Elk()
        try:
            data = e.get_sDevID_data(userid)
            scaled_data = e.preprocessing_data(data)
            scaled_data.rename({'cRes' : '차단 여부', 'sDevID': '가입자 ID', 'uDstIp': '접속 IP 주소', 'uDstPort': '접속 포트', 'sHost': '접속 주소', 'sURI':'URI', 'sUA':'유저 에이전트', 'timestamp':'접속 시간', 'sRef': '이전 접속 주소', 'nSize': '패킷 길이'}, axis=1, inplace=True)
            scaled_data.drop(['hour', 'URI', 'sMwN', '가입자 ID','이전 접속 주소', 'minute', 'duration', 'previous_sHost', 'sHost_same_as_previous', 'sHost_same_as_previous_count'], axis=1, inplace=True)
            scaled_data['접속 시간'] = scaled_data['접속 시간'].apply(lambda x : str(x).split('.')[0])
             
            data_return = True
        except:
            error = "No exist User Id or logs"
            flash(error)
       
        return render_template('user_data.html',  form=form, scaled_data=scaled_data, data_return=data_return, data=data)

    return render_template('user_data.html', form=form,  scaled_data=scaled_data, data_return=data_return, data=data)


@bp.route('/download_excel', methods=['POST'])
@login_required
def download_excel():
    now = datetime.now()
    # 한국 시간대로 변환
    korea_timezone = pytz.timezone("Asia/Seoul")
    korea_time = now.astimezone(korea_timezone)

    # 날짜 문자열 추출
    korea_date = korea_time.strftime("%Y-%m-%d %H:%M")
    data_json = request.form['data']
    user_id = request.form['user_name']
    scaled_data = pd.read_json(data_json)

    # Convert the DataFrame to an in-memory Excel file
    excel_file = BytesIO()
    scaled_data.to_excel(excel_file, index=False)
    excel_file.seek(0)

    # Create a response object with the Excel data
    response = Response(
        excel_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Set the file download headers
    response.headers['Content-Disposition'] = f'attachment; filename={user_id}_{korea_date}.xlsx'

    return response





# form = UserLoginForm()

#     if request.method == "POST" and form.validate_on_submit():
      

#         if error is None:
#             session.clear()
#             session['user_id'] = user.id
#             _next = request.args.get('next', '')
#             if _next:
#                 return redirect(_next)
#             else:
#                 return redirect(url_for('main.home'))

#         flash(error)
#     return render_template('auth/login.html', form=form)

