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

import openpyxl
# main_views가 인수로 전달, 첫 번째 인수 main은 블루프린트의 별칭
bp = Blueprint('model', __name__, url_prefix='/model')



@bp.route('/show_models/', methods=('GET', 'POST'))
@login_required
def show_model():
    form = UserSearchId()
    data_return = False

    if request.method == "POST" and form.validate_on_submit():
        error = None
        userid = form.userid.data
        m = Modeling() 
        e = Elk()
        dec_data = e.get_final_dec_data_dev_id(userid)
        data_return = True
        model_list = m.total_model_load()

        kmeans_outlier_k = m.get_kmeans_outlier_k()
        kmeans_label, rf_label, gm_label, isof_label = m.return_labels(dec_data, model_list)

        label_list = ["정상"]
        outlier_count = 0
        if dec_data['접속 시간(분)'].values <= 30 or dec_data['평균 접속 수(1분)'].values <= 1:
            label_list[0] = '비정상'
            outlier_count = 1

        if dec_data["차단 수"].values >= 10 or dec_data["차단율(%)"].values >= 50:
            label_list[0] = '비정상'
            outlier_count = 1

        
        if dec_data["평균 접속 수(1분)"].values >= 100 and dec_data["최다 이용 UA 접속 비율(%)"].values >= 95 and dec_data["최대 빈도 URL 접속 비율(%)"].values >= 95:
            label_list[0] = '비정상'
            outlier_count = 1

        
        if dec_data["최다 접속 URL"].values == "123.57.193.95" or dec_data["최다 접속 URL"].values == "123.57.193.52":
            label_list[0] = '비정상'
            outlier_count = 1

        if kmeans_label == kmeans_outlier_k:
            outlier_count += 1
            label_list.append(f'비정상(label : {kmeans_outlier_k})')
        else:
            label_list.append(f'정상(label : {kmeans_label})')
            
        if rf_label == 1:
            label_list.append(f'비정상(label : {rf_label})')
            outlier_count += 1
        else:
            label_list.append(f'정상(label : {rf_label})')
            
        if gm_label == 1:
            label_list.append(f'비정상(label : {gm_label})')
            outlier_count += 1
        else:
            label_list.append(f'정상(label : {gm_label})')


        if isof_label == -1:
            label_list.append(f'비정상(label : {isof_label})')
            outlier_count += 1
        else:
            label_list.append(f'정상(label : {isof_label})')

        label_list.append(outlier_count)

        custom_column_names = ['Rule-based', 'K-Means', 'Random Forest', 'Gaussian Mixture', 'Isolation Forest', 'Anomaly Detection Count']

        # Creating a DataFrame with custom column names
        label_data = {custom_column_names[i]: [label_list[i]] for i in range(len(label_list))}
        df = pd.DataFrame(label_data)



        return render_template('show_model.html', form=form, data_return=data_return, df=df, dec_data=dec_data)
    
    return render_template('show_model.html', form=form)

@bp.route('/save_anomaly_db', methods=['POST'])
@login_required
def save_db():
    
    return_data = request.form['data']
    
    return_df = request.form['df']

    dec_data = pd.read_json(return_data)
    df = pd.read_json(return_df)
    e = Elk()

    e.save_db_data(dec_data, "abnormal_describe")   

    # Replace 'current_page' with the endpoint of the current page you want to redirect to
    return render_template('show_model.html', form=None, data_return=True, df=df, dec_data=dec_data)
# @bp.route('/abnormaly_board/')
# @login_required
# def abnormaly_board():
#     return render_template('abnormaly_user_board.html')
    


# @bp.route('/search/', methods=('GET', 'POST'))
# @login_required
# def user_dashboard():
#     form = UserSearchId()
#     graphJSON = False
#     if request.method == "POST" and form.validate_on_submit():
#         error = None
#         userid = form.userid.data
#         dash = Modeling()
#         try:
#             fig = dash.get_device_id_dash(userid)
#             graphJSON = fig.to_json()
#         except:
#             error = "No exist User Id or logs"
#             flash(error)
       
#         return render_template('user_dashboard.html',  form=form, graphJSON=graphJSON)

#     return render_template('user_dashboard.html', form=form, graphJSON=graphJSON)


