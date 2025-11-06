import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from config import Config
from app.models.profile import Profile, Field


class ProfilesService:
    """Servicio para gestionar perfiles de mapeo"""
    
    def __init__(self):
        self.profiles_dir = Config.PROFILES_DIR
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Obtiene todos los perfiles guardados"""
        profiles = []
        for profile_file in self.profiles_dir.glob('*.json'):
            try:
                with open(profile_file, 'r', encoding='utf-8') as f:
                    profile_data = json.load(f)
                    profiles.append(profile_data)
            except Exception as e:
                print(f"Error loading profile {profile_file}: {e}")
        
        return sorted(profiles, key=lambda x: x.get('fecha_creacion', ''), reverse=True)
    
    def get_profile(self, profile_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un perfil por su ID"""
        profile_file = self.profiles_dir / f"{profile_id}.json"
        
        if not profile_file.exists():
            return None
        
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading profile {profile_id}: {e}")
            return None
    
    def create_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un nuevo perfil"""
        try:
            # Crear objeto Profile
            profile = Profile.from_dict(profile_data)
            
            # Guardar perfil
            profile_file = self.profiles_dir / f"{profile.id}.json"
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(profile.to_json())
            
            return profile.to_dict()
        
        except Exception as e:
            raise Exception(f"Error creating profile: {str(e)}")
    
    def update_profile(self, profile_id: str, profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualiza un perfil existente"""
        profile_file = self.profiles_dir / f"{profile_id}.json"
        
        if not profile_file.exists():
            return None
        
        try:
            # Actualizar fecha de modificación
            profile_data['id'] = profile_id
            profile_data['fecha_actualizacion'] = datetime.now().isoformat()
            
            # Crear objeto Profile
            profile = Profile.from_dict(profile_data)
            
            # Guardar perfil actualizado
            with open(profile_file, 'w', encoding='utf-8') as f:
                f.write(profile.to_json())
            
            return profile.to_dict()
        
        except Exception as e:
            raise Exception(f"Error updating profile: {str(e)}")
    
    def delete_profile(self, profile_id: str) -> bool:
        """Elimina un perfil"""
        profile_file = self.profiles_dir / f"{profile_id}.json"
        
        if not profile_file.exists():
            return False
        
        try:
            profile_file.unlink()
            return True
        except Exception as e:
            print(f"Error deleting profile {profile_id}: {e}")
            return False
    
    def search_profiles(self, query: str) -> List[Dict[str, Any]]:
        """Busca perfiles por nombre o descripción"""
        all_profiles = self.get_all_profiles()
        query_lower = query.lower()
        
        return [
            p for p in all_profiles
            if query_lower in p.get('nombre', '').lower() or
               query_lower in p.get('descripcion', '').lower()
        ]
