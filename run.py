from app import create_app
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Wybierz konfigurację na podstawie zmiennej środowiskowej
config_name = os.getenv('FLASK_CONFIG', 'config.DevelopmentConfig')
app = create_app(config_name)

if __name__ == '__main__':
    # Pobierz port z zmiennej środowiskowej lub użyj domyślnego 5000
    port = int(os.environ.get('PORT', 5000))
    
    # W trybie produkcyjnym używaj 0.0.0.0 aby aplikacja była dostępna z zewnątrz
    host = '0.0.0.0' if os.environ.get('FLASK_ENV') == 'production' else '127.0.0.1'
    
    app.run(host=host, port=port)