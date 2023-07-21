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
   
    if request.method == "POST" and form.validate_on_submit():
        error = None
        userid = form.userid.data

        return render_template('show_model.html', form=form)
    
    return render_template('show_model.html', form=form)
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


