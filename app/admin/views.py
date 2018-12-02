from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from . import admin
from ..models import User


@admin.route("/", methods=["GET", "POST"])
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """

    # Make sure user is authorized
    if not current_user.is_admin:
        return redirect(url_for("home.dashboard"))

    # Perform admin action
    if request.method == "POST":
        user_id = int(request.form['userId'])
        user = User.query.filter_by(id=user_id).first()
        if request.form['action'] == 'Delete':
            db.session.delete(user)
        elif request.form['action'] == 'Make Admin':
            user.is_admin = True
        db.session.commit()

    response_data = {}

    response_data["users"] = User.query.all()

    # load registration template
    return render_template("admin.html", response_data=response_data, title="Admin", current_user=current_user)