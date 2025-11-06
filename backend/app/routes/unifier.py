from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.services.unifier_service import UnifierService
from config import Config

bp = Blueprint('unifier', __name__, url_prefix='/api/unifier')
service = UnifierService()


@bp.route('/unify', methods=['POST'])
def unify_files():
    """Unifica múltiples archivos Excel en uno solo"""
    try:
        # Verificar si hay archivos
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files or len(files) == 0:
            return jsonify({'error': 'No files provided'}), 400
        
        # Parámetros adicionales
        output_name = request.form.get('output_name', 'unificado.xlsx')
        remove_duplicates = request.form.get('remove_duplicates', 'false').lower() == 'true'
        add_source_column = request.form.get('add_source_column', 'true').lower() == 'true'
        
        # Guardar archivos temporalmente
        file_paths = []
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            file_path = Config.UPLOADS_DIR / filename
            file.save(str(file_path))
            file_paths.append(str(file_path))
        
        if not file_paths:
            return jsonify({'error': 'No valid files provided'}), 400
        
        # Unificar archivos
        result = service.unify_files(
            file_paths, 
            output_name, 
            remove_duplicates, 
            add_source_column
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/normalize-columns', methods=['POST'])
def normalize_columns():
    """Normaliza nombres de columnas de un archivo"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        column_mapping = service.normalize_column_names(str(file_path))
        
        return jsonify({'column_mapping': column_mapping}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
