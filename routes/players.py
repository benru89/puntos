from flask import Blueprint, render_template, request
from models import Player, TrainingPoints
from extensions import db
import datetime
import calendar

players_bp = Blueprint('players', __name__, template_folder='../templates')

@players_bp.route('/players', methods=['GET'])
def list_players():
    year = request.args.get('year', type=int, default=datetime.date.today().year)
    month = request.args.get('month', type=int, default=datetime.date.today().month)

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

    players = Player.query.all()

    points_query = TrainingPoints.query.filter(
        TrainingPoints.date.between(first_day, last_day)
    ).all()

    # Fix: clearly build the nested dictionary correctly
    training_points = {}
    training_dates = set()

    for tp in points_query:
        training_dates.add(tp.date)
        if tp.player_id not in training_points:
            training_points[tp.player_id] = {}
        training_points[tp.player_id][tp.date] = tp.points

    training_dates = sorted(training_dates)

    return render_template('players.html',
                           players=players,
                           training_points=training_points,
                           training_dates=training_dates,
                           month=month,
                           year=year)
