from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import redirect
from monitoring.views.auth_views import login_required

from monitoring.forms import UserSearchId
# from elk.segment import * 
# from pybo.models import Question

# main_views가 인수로 전달, 첫 번째 인수 main은 블루프린트의 별칭
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/search/', methods=('GET', 'POST'))
@login_required
def search():
    form = UserSearchId()
    if request.method == "POST" and form.validate_on_submit():
        
        userid = form.userid.data
        return userid

    
    # flash(error)
    # current_app.logger.info("info")
    # return redirect(url_for('question._list'))
    return render_template('user_search.html', form=form)


    

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

