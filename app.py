import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainings.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register Blueprints
    from routes.players import players_bp
    from routes.training import training_bp
    app.register_blueprint(players_bp)
    app.register_blueprint(training_bp)

    # Optional: A simple home route
    @app.route('/')
    def index():
        return "Welcome to the Training App! Go to /players or /training."

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    # Listen on the port provided by the environment or default to 5000
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
