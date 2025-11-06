from flask import Blueprint, request, jsonify
from app.services.profiles_service import ProfilesService

bp = Blueprint('profiles', __name__, url_prefix='/api/profiles')
service = ProfilesService()


@bp.route('', methods=['GET'])
def get_all_profiles():
    """Obtiene todos los perfiles"""
    try:
        profiles = service.get_all_profiles()
        return jsonify(profiles), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/<profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Obtiene un perfil por ID"""
    try:
        profile = service.get_profile(profile_id)
        
        if profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify(profile), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('', methods=['POST'])
def create_profile():
    """Crea un nuevo perfil"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        profile = service.create_profile(data)
        return jsonify(profile), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/<profile_id>', methods=['PUT'])
def update_profile(profile_id):
    """Actualiza un perfil existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        profile = service.update_profile(profile_id, data)
        
        if profile is None:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify(profile), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@bp.route('/<profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Elimina un perfil"""
    try:
        success = service.delete_profile(profile_id)
        
        if not success:
            return jsonify({'error': 'Profile not found'}), 404
        
        return jsonify({'message': 'Profile deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/search', methods=['GET'])
def search_profiles():
    """Busca perfiles por query"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        profiles = service.search_profiles(query)
        return jsonify(profiles), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
