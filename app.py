from flask import Flask
from dotenv import load_dotenv
import os
from routes import configure_routes

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY')
    
    # Configuration for Spotify API
    app.config['CLIENT_ID'] = os.environ.get('CLIENT_ID')
    app.config['CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')
    app.config['REDIRECT_URI'] = 'http://localhost:5000/redirect'
    
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
