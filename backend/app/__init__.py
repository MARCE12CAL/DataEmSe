from flask import Flask
from flask_cors import CORS
from config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # CORS - Permitir todo
    CORS(app)
    
    # Registrar blueprints
    from app.routes import profiles, autodetect, batch, scanner, unifier, comparator, exporter
    
    app.register_blueprint(profiles.bp)
    app.register_blueprint(autodetect.bp)
    app.register_blueprint(batch.bp)
    app.register_blueprint(scanner.bp)
    app.register_blueprint(unifier.bp)
    app.register_blueprint(comparator.bp)
    app.register_blueprint(exporter.bp)
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    return app