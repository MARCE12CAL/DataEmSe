from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.comparator_service import ComparatorService
from config import Config

bp = Blueprint('comparator', __name__, url_prefix='/api/comparator')
service = ComparatorService()


@bp.route('/compare', methods=['POST'])
def compare_file():
    """Compara un archivo Excel contra un modelo"""
    try:
        # Verificar archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Obtener columnas del modelo
        model_columns = request.form.get('model_columns')
        
        if not model_columns:
            return jsonify({'error': 'model_columns is required'}), 400
        
        # Convertir string JSON a lista
        import json
        try:
            model_columns = json.loads(model_columns)
        except:
            return jsonify({'error': 'Invalid model_columns format'}), 400
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        # Comparar archivo
        result = service.compare_with_model(str(file_path), model_columns)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/report/<report_name>', methods=['GET'])
def get_report(report_name):
    """Obtiene un reporte de comparación guardado"""
    try:
        report = service.get_comparison_report(report_name)
        
        if report is None:
            return jsonify({'error': 'Report not found'}), 404
        
        return jsonify(report), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
