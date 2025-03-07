from flask import Blueprint, render_template, request, redirect, url_for
from models import TrainingPoints, Player
from extensions import db
import datetime

training_bp = Blueprint('training', __name__, template_folder='../templates')

@training_bp.route('/training', methods=['GET', 'POST'])
def training():
    players = Player.query.all()

    if request.method == 'POST':
        date_str = request.form.get('date')
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        for player in players:
            points_str = request.form.get(f'points_{player.id}')
            if points_str and points_str.isdigit():
                points = int(points_str)

                existing_entry = TrainingPoints.query.filter_by(player_id=player.id, date=date_obj).first()
                if existing_entry:
                    existing_entry.points = points
                else:
                    new_points = TrainingPoints(player_id=player.id, points=points, date=date_obj)
                    db.session.add(new_points)

        db.session.commit()
        
        # Redirect back to the same date to maintain the state
        return redirect(url_for('training.training', date=date_str))

    # Handle date from GET params or default to today
    date_str = request.args.get('date')
    if date_str:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_obj = datetime.date.today()

    existing_points_query = TrainingPoints.query.filter_by(date=date_obj).all()
    existing_points = {tp.player_id: tp.points for tp in existing_points_query}

    return render_template(
        'training.html',
        players=players,
        existing_points=existing_points,
        date=date_obj.strftime('%Y-%m-%d')
    )
