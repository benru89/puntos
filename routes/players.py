from flask import Blueprint, render_template, request, redirect, url_for
from models import Player, TrainingPoints
from extensions import db
import datetime, calendar

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

    training_points = {}
    for tp in points_query:
        if tp.player_id not in training_points:
            training_points[tp.player_id] = {}
        training_points[tp.player_id][tp.date] = tp.points

    training_dates = sorted({tp.date for tp in points_query})

    return render_template('players.html',
                           players=players,
                           training_points=training_points,
                           training_dates=training_dates,
                           month=month,
                           year=year)

@players_bp.route('/add_player', methods=['POST'])
def add_player():
    name = request.form.get('name')
    if name:
        nuevo_jugador = Player(name=name)
        db.session.add(nuevo_jugador)
        db.session.commit()
    return redirect(url_for('players.list_players'))

@players_bp.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    # Also remove associated training points (optional but recommended)
    TrainingPoints.query.filter_by(player_id=player.id).delete()
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('players.list_players'))
