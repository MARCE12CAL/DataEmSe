from flask import Blueprint, request, jsonify
from app.services.scanner_service import ScannerService

bp = Blueprint('scanner', __name__, url_prefix='/api/scanner')
service = ScannerService()


@bp.route('/scan', methods=['POST'])
def scan_folder():
    """Escanea una carpeta en busca de archivos Excel"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        folder_path = data.get('folder_path')
        recursive = data.get('recursive', True)
        
        if not folder_path:
            return jsonify({'error': 'folder_path is required'}), 400
        
        result = service.scan_folder(folder_path, recursive)
        
        return jsonify(result), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/generate-config', methods=['POST'])
def generate_config():
    """Genera CSV de configuración para procesamiento batch"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        files = data.get('files', [])
        output_path = data.get('output_path', 'batch_config.csv')
        
        if not files:
            return jsonify({'error': 'No files provided'}), 400
        
        csv_path = service.generate_config_csv(files, output_path)
        
        return jsonify({
            'message': 'Config CSV generated successfully',
            'csv_path': csv_path
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
