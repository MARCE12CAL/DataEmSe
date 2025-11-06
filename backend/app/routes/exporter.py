from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.services.exporter_service import ExporterService
from config import Config

bp = Blueprint('exporter', __name__, url_prefix='/api/exporter')
service = ExporterService()


@bp.route('/export', methods=['POST'])
def export_file():
    """Exporta un archivo Excel a otros formatos"""
    try:
        # Verificar archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Obtener parámetros
        formats = request.form.get('formats', 'csv')  # csv, json, sql
        table_name = request.form.get('table_name', 'data')
        database_type = request.form.get('database_type', 'postgresql')
        
        # Convertir formats a lista
        if isinstance(formats, str):
            formats = [f.strip() for f in formats.split(',')]
        
        # Guardar archivo temporalmente
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        # Exportar a múltiples formatos
        results = service.export_multiple_formats(str(file_path), formats)
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/export-csv', methods=['POST'])
def export_csv():
    """Exporta archivo a CSV"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        delimiter = request.form.get('delimiter', ',')
        output_name = request.form.get('output_name')
        
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        csv_path = service.export_to_csv(str(file_path), output_name, delimiter)
        
        return jsonify({'csv_path': csv_path}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/export-json', methods=['POST'])
def export_json():
    """Exporta archivo a JSON"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        orient = request.form.get('orient', 'records')
        output_name = request.form.get('output_name')
        
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        json_path = service.export_to_json(str(file_path), output_name, orient)
        
        return jsonify({'json_path': json_path}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/export-sql', methods=['POST'])
def export_sql():
    """Exporta archivo a SQL"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        table_name = request.form.get('table_name', 'data')
        database_type = request.form.get('database_type', 'postgresql')
        output_name = request.form.get('output_name')
        
        filename = secure_filename(file.filename)
        file_path = Config.UPLOADS_DIR / filename
        file.save(str(file_path))
        
        sql_path = service.export_to_sql(
            str(file_path), 
            table_name, 
            database_type, 
            output_name
        )
        
        return jsonify({'sql_path': sql_path}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
