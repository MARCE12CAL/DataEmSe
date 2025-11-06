from flask import Blueprint, request, jsonify, send_file
from app.services.batch_service import BatchService
from config import Config
import io

bp = Blueprint('batch', __name__, url_prefix='/api/batch')
service = BatchService()


@bp.route('/generate-script', methods=['POST'])
def generate_script():
    """Genera un script Python para procesamiento batch"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        profile_name = data.get('profile_name')
        csv_path = data.get('csv_path')
        output_folder = data.get('output_folder')
        file_prefix = data.get('file_prefix', 'procesado')
        
        if not all([profile_name, csv_path, output_folder]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        script = service.generate_batch_script(
            profile_name, 
            csv_path, 
            output_folder, 
            file_prefix
        )
        
        return jsonify({
            'script': script,
            'filename': f'batch_processor_{profile_name}.py'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/download-script', methods=['POST'])
def download_script():
    """Descarga el script generado"""
    try:
        data = request.get_json()
        script = data.get('script')
        filename = data.get('filename', 'batch_processor.py')
        
        if not script:
            return jsonify({'error': 'No script provided'}), 400
        
        # Crear archivo en memoria
        script_bytes = script.encode('utf-8')
        buffer = io.BytesIO(script_bytes)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='text/x-python'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/save-job', methods=['POST'])
def save_job():
    """Guarda configuración de un job batch"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        job_name = data.get('job_name')
        config = data.get('config')
        
        if not job_name or not config:
            return jsonify({'error': 'Missing required fields'}), 400
        
        job_path = service.save_batch_job(job_name, config)
        
        return jsonify({
            'message': 'Job saved successfully',
            'job_path': job_path
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/get-job/<job_name>', methods=['GET'])
def get_job(job_name):
    """Obtiene configuración de un job batch"""
    try:
        job_config = service.get_batch_job(job_name)
        
        if job_config is None:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job_config), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
