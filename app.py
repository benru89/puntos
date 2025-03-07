# app.py
import os
from flask import Flask
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainings.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from routes.players import players_bp
        from routes.training import training_bp

        app.register_blueprint(players_bp)
        app.register_blueprint(training_bp)

        db.create_all()

    @app.route('/')
    def index():
        return "Welcome to the Training App! Go to /players or /training."

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
