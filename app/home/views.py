from flask import render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, func
from . import home, helper
from ..models import Ai, GameLog, User
from app import db
from datetime import datetime



@home.route("/", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    Render dashboard
    """
    response_data = {}

    # Get users AI
    users_ai = Ai.query.filter_by(user=current_user).first()

    if users_ai:
        response_data["games_won"] = GameLog.query.filter_by(ai_won=users_ai, is_draw=False).count()
        response_data["games_lost"] = GameLog.query.filter_by(ai_lost=users_ai, is_draw=False).count()
        response_data["games_drawn"] = GameLog.query.filter(or_(GameLog.ai_won == users_ai, GameLog.ai_lost == users_ai), GameLog.is_draw == True).count()
        response_data["last_uploaded"] = users_ai.uploaded_on.strftime("%d/%m/%y")

        # Get recent games
        response_data["recent_games"] = GameLog.query.filter(or_(GameLog.ai_won == users_ai,
                                                                 GameLog.ai_lost == users_ai)).order_by(GameLog.timestamp.desc()).limit(5)
    else:
        response_data["games_won"] = 0
        response_data["games_lost"] = 0
        response_data["games_drawn"] = 0
        response_data["last_uploaded"] = "Never"
        response_data["recent_games"] = {}

    if request.method == "POST" and "ai_file" in request.files:
        file = request.files["ai_file"]

        if file.filename == "":
            response_data["file_message"] = "invalid file"
        else:
            # Send file to S3
            s3_filename = str(current_user.id) + "_" + current_user.username + "." + file.filename.split('.')[-1]
            filename = helper.upload_file_to_s3(file, s3_filename)
            # Save new details in database
            if filename:
                if users_ai:
                    users_ai.filename = s3_filename
                    users_ai.uploaded_on = datetime.utcnow()
                else:
                    users_ai = Ai(user=current_user, filename=s3_filename)
                    db.session.add(users_ai)
                db.session.commit()
                response_data["file_message"] = "uploaded Successfully!"



    return render_template("index.html", title="Dashboard", first_name=current_user.first_name,
                           response_data = response_data)


@home.route("/rules")
@login_required
def rules():
    return render_template("rules.html", title="Game Rules")


@home.route("/game_logs")
@login_required
def game_logs():
    response_data = {}
    # Get users AI
    users_ai = Ai.query.filter_by(user=current_user).first()
    if users_ai:
        # Get recent games
        response_data["recent_games"] = GameLog.query.filter(or_(GameLog.ai_won == users_ai,
                                                                 GameLog.ai_lost == users_ai)).order_by(GameLog.timestamp.desc()).limit(20)

    return render_template("game_logs.html", title="My Game Logs", response_data = response_data)

@home.route("/standings")
@login_required
def standings():

    sql = "SELECT t2.id as id, t1.username as name FROM users t1 LEFT JOIN ais t2 ON t2.user_id = t1.id"

    sql2 = "SELECT s1.*, COUNT(s2.ai_lost_id) as losses FROM (" + sql + \
           ")s1 LEFT JOIN (SELECT * FROM game_log WHERE is_draw = FALSE)s2 ON s1.id = s2.ai_lost_id GROUP BY name"
    
    sql3 = "SELECT s1.*, COUNT(s2.ai_won_id) as wins FROM (" + sql2 + \
           ")s1 LEFT JOIN (SELECT * FROM game_log WHERE is_draw = FALSE)s2 ON s1.id = s2.ai_won_id GROUP BY name"

    sql4 = "SELECT v1.*, COUNT(v2.id) as draws FROM (" + \
        sql3 + ")v1 LEFT JOIN (SELECT * FROM game_log WHERE is_draw = TRUE) v2 ON v1.id = v2.ai_won_id OR " \
               "v1.id = v2.ai_lost_id GROUP BY name ORDER BY wins DESC, draws DESC, losses ASC"

    ai_list = db.engine.execute(sql4)
    users_ai = Ai.query.filter_by(user=current_user).first()

    return render_template("standings.html", title="Standings", ai_list=ai_list, my_ai=users_ai.id)
