from flask import Flask
from config import Config
from models import db, Admin
from controllers.store_controller import store_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__, template_folder='views')
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(store_bp)
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()
    if not Admin.query.first():
        db.session.add(Admin(usuario='admin', clave='onixz'))
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)