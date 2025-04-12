from flask import Flask
import logging

from app.database import db

logging.basicConfig(level=logging.INFO)


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

from app.routes.health_routes import health_blueprint
from app.routes.screenshot_routes import screenshot_blueprint

app.register_blueprint(health_blueprint)
app.register_blueprint(screenshot_blueprint, url_prefix='/screenshots')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
