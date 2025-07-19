from dotenv import load_dotenv
load_dotenv()
import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.email_service import email_service
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import User
from src.models.user import db, User
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.reunioes import reunioes_bp
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'agendador-reunioes-secret-key-2025'

# Configurar CORS para permitir requisições do frontend
CORS(app, supports_credentials=True)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(reunioes_bp, url_prefix='/api')

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
print(f"DEBUG: SQLALCHEMY_DATABASE_URI = {os.environ.get('SQLALCHEMY_DATABASE_URI')}")
db.init_app(app)

def create_admin_user():
    """Criar usuário administrador padrão se não existir"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='agendamontereletrica@gmail.com',
            is_admin=True
        )
        admin.set_password('admin123')  # Senha padrão - deve ser alterada
        db.session.add(admin)
        db.session.commit()
        print("Usuário administrador criado:")
        print("Username: admin")
        print("Senha: admin123")
        

with app.app_context():
    db.create_all()
    create_admin_user()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)