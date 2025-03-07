from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from models import TrainingPoints, Player
import datetime

training_bp = Blueprint('training', __name__, template_folder='../templates')

@training_bp.route('/training', methods=['GET', 'POST'])
def training():
    players = Player.query.all()

    if request.method == 'POST':
        date_str = request.form.get('date', datetime.date.today().strftime('%Y-%m-%d'))
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        for player in players:
            field_name = f'points_{player.id}'
            points_str = request.form.get(field_name)
            if points_str and points_str.isdigit():
                points = int(points_str)
                existing_entry = TrainingPoints.query.filter_by(player_id=player.id, date=date_obj).first()
                if existing_entry:
                    existing_entry.points = points
                else:
                    new_entry = TrainingPoints(player_id=player.id, points=points, date=date_obj)
                    db.session.add(new_entry)
            elif points_str == '':
                # Handle empty input as deletion of existing points
                TrainingPoints.query.filter_by(player_id=player.id, date=date_obj).delete()

        db.session.commit()
        return redirect(url_for('training.training', date=date_str))

    # Handle GET request
    date_str = request.args.get('date', datetime.date.today().strftime('%Y-%m-%d'))
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    existing_entries = TrainingPoints.query.filter_by(date=date_obj).all()
    existing_points = {tp.player_id: tp.points for tp in existing_entries}

    return render_template('training.html',
                           players=players,
                           existing_points=existing_points,
                           date=date_obj.strftime('%Y-%m-%d'))
