import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainings.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Register Blueprints here (if you have any)
    from routes.players import players_bp
    from routes.training import training_bp
    app.register_blueprint(players_bp)
    app.register_blueprint(training_bp)

    @app.route('/')
    def index():
        return "Welcome to the Training App! Go to /players or /training."

    return app

app = create_app()  # <-- explicitly create app instance here

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
