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

    # Sort players by total points (lowest to highest)
    players_sorted = sorted(players, key=lambda p: total_points[p.id], reverse=True)
   
    # Fechas de entrenamiento únicas ordenadas
    training_dates = sorted({tp.date for tp in points_query})

    last_red_index = None

    if len(players_sorted) > 10:
        threshold_red = total_points[players_sorted[-6].id]  # Bottom 7 threshold

    for index, player in enumerate(players_sorted):
        if total_points[player.id] <= threshold_red:
            last_red_index = index  # Store last red player index
            break

    # Pass last_red_index to template
    return render_template(
        'players.html',
        players=players_sorted,
        total_points=total_points,
        training_points=training_points,
        training_dates=training_dates,
        last_red_index=last_red_index,  
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