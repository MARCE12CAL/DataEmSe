from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json
from datetime import datetime

@dataclass
class Field:
    """Representa un campo en un perfil de mapeo"""
    nombre: str
    palabras_clave: List[str]
    tipo_dato: str = 'texto'
    requerido: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nombre': self.nombre,
            'palabras_clave': self.palabras_clave,
            'tipo_dato': self.tipo_dato,
            'requerido': self.requerido
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Field':
        return cls(
            nombre=data['nombre'],
            palabras_clave=data['palabras_clave'],
            tipo_dato=data.get('tipo_dato', 'texto'),
            requerido=data.get('requerido', False)
        )


@dataclass
class Profile:
    """Representa un perfil de mapeo de datos"""
    nombre: str
    descripcion: str
    campos: List[Field]
    id: str = None
    fecha_creacion: str = None
    fecha_actualizacion: str = None
    
    def __post_init__(self):
        if self.id is None:
            self.id = f"profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        if self.fecha_creacion is None:
            self.fecha_creacion = datetime.now().isoformat()
        if self.fecha_actualizacion is None:
            self.fecha_actualizacion = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'campos': [campo.to_dict() for campo in self.campos],
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Profile':
        campos = [Field.from_dict(c) for c in data.get('campos', [])]
        return cls(
            id=data.get('id'),
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            campos=campos,
            fecha_creacion=data.get('fecha_creacion'),
            fecha_actualizacion=data.get('fecha_actualizacion')
        )
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Profile':
        data = json.loads(json_str)
        return cls.from_dict(data)
