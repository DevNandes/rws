"""
Ponto de entrada para o Gunicorn

"""
from app import create_app

application = create_app()

# EOF
