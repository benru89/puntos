from flask import Blueprint, render_template, request, redirect, url_for
from models import Player
from app import db

players_bp = Blueprint('players', __name__, template_folder='../templates')

@players_bp.route('/players')
def list_players():
    players = Player.query.all()
    return render_template('players.html', players=players)

@players_bp.route('/add_player', methods=['POST'])
def add_player():
    name = request.form.get('name')
    if name:
        new_player = Player(name=name)
        db.session.add(new_player)
        db.session.commit()
    return redirect(url_for('players.list_players'))
