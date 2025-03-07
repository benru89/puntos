from flask import Blueprint, render_template, redirect, url_for, request
from extensions import db
from models import Player, TrainingPoints
import datetime, calendar
from collections import defaultdict

players_bp = Blueprint('players', __name__, template_folder='../templates')

@players_bp.route('/', methods=['GET'])
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

    training_points = defaultdict(dict)
    total_points = defaultdict(int)

    for tp in points_query:
        training_points[tp.player_id][tp.date.strftime('%Y-%m-%d')] = tp.points
        total_points[tp.player_id] += tp.points

    # Ordena los jugadores por puntos totales (mayor a menor)
    players_sorted = sorted(players, key=lambda p: total_points[p.id], reverse=True)

    # Fechas de entrenamiento únicas ordenadas
    training_dates = sorted({tp.date for tp in points_query})

    return render_template(
        'players.html',
        players=players_sorted,
        training_dates=training_dates,
        training_points=training_points,
        total_points=total_points,
        month=month,
        year=year
    )

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
    jugador = Player.query.get_or_404(player_id)
    db.session.delete(jugador)
    db.session.commit()
    return redirect(url_for('players.list_players'))