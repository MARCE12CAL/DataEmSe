from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.autodetect_service import AutoDetectService
from config import Config
import os

bp = Blueprint('autodetect', __name__, url_prefix='/api/autodetect')
service = AutoDetectService()


@bp.route('/analyze', methods=['POST'])
def analyze_files():
    """Analiza archivos Excel para auto-detectar campos"""
    try:
        # Verificar si hay archivos
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        # Guardar archivos temporalmente
        file_paths = []
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            file_path = Config.TEMP_MUESTRAS_DIR / filename
            file.save(str(file_path))
            file_paths.append(str(file_path))
        
        if not file_paths:
            return jsonify({'error': 'No valid files provided'}), 400
        
        # Analizar archivos
        result = service.analyze_files(file_paths)
        
        # Limpiar archivos temporales
        for file_path in file_paths:
            try:
                os.remove(file_path)
            except:
                pass
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/create-profile', methods=['POST'])
def create_profile_from_detection():
    """Crea un perfil desde campos detectados"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        detected_fields = data.get('detected_fields', [])
        profile_name = data.get('profile_name', 'Auto-detected Profile')
        profile_description = data.get('profile_description', '')
        
        if not detected_fields:
            return jsonify({'error': 'No detected fields provided'}), 400
        
        profile_data = service.create_profile_from_detection(
            detected_fields, 
            profile_name, 
            profile_description
        )
        
        return jsonify(profile_data), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
