from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import redirect
from monitoring.forms import UserLoginForm
from monitoring.models import User
import functools


# main_views가 인수로 전달, 첫 번째 인수 main은 블루프린트의 별칭
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login/',  methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('main.home'))

    form = UserLoginForm()

    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "Non-existent user"
        elif not check_password_hash(user.password, form.password.data):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.home'))

        flash(error)
    return render_template('auth/login.html', form=form)

    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

# @bp.route('/login/', methods=('GET', 'POST'))
# def login():
#     form = UserLoginForm()
#     if request.method == "POST" and form.validate_on_submit():
#         error = None
#         user = User.query.filter_by(username=form.username.data).first()
#         if not user:
#             error = "Non-existent user"
#         elif not check_password_hash(user.password, form.password.data):
#             error = "Incorrect password"
#         if error is None:
#             session.clear()
#             session['user_id'] = user.id
#             _next = request.args.get('next', '')
#             if _next:
#                 return redirect(_next)
#             else:
#                 return redirect(url_for('main.index'))
#         flash(error)
#     return render_template('auth/login.html', form=form)