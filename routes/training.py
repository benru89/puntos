from flask import Blueprint, render_template, request, redirect, url_for
from models import TrainingPoints, Player
from app import db
import datetime

training_bp = Blueprint('training', __name__, template_folder='../templates')

@training_bp.route('/training')
def training():
    players = Player.query.all()
    return render_template('training.html', players=players)

@training_bp.route('/add_points', methods=['POST'])
def add_points():
    player_id = request.form.get('player_id')
    points = request.form.get('points')
    date_str = request.form.get('date')
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.date.today()
    if player_id and points:
        new_points = TrainingPoints(player_id=player_id, points=points, date=date_obj)
        db.session.add(new_points)
        db.session.commit()
    return redirect(url_for('training.training'))
