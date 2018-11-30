from flask import render_template
from flask_login import login_required, current_user

from . import home



@home.route('/')
@login_required
def dashboard():
    """
    Render dashboard
    """

    return render_template('index.html', title="Dashboard", first_name=current_user.first_name)