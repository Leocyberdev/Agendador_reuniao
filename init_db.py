import sys
import os

# Adiciona o caminho do projeto para encontrar 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src import create_app
from src.models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso.")

