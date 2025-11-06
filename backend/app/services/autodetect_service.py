import pandas as pd
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from config import Config


class AutoDetectService:
    """Servicio para auto-detectar campos en archivos Excel"""
    
    # Patrones comunes para detección
    PATRONES = {
        'cedula': [r'c[eé]dula', r'ci\b', r'identificaci[oó]n', r'documento', r'ruc'],
        'nombre': [r'nombre', r'apellido', r'raz[oó]n social', r'cliente'],
        'email': [r'email', r'correo', r'e-mail', r'mail'],
        'telefono': [r'tel[eé]fono', r'celular', r'móvil', r'tel\b', r'cel\b'],
        'direccion': [r'direcci[oó]n', r'domicilio', r'ubicaci[oó]n'],
        'fecha': [r'fecha', r'date', r'día'],
        'monto': [r'monto', r'valor', r'precio', r'total', r'importe', r'cantidad'],
        'codigo': [r'c[oó]digo', r'code', r'id\b', r'num', r'número'],
        'descripcion': [r'descripci[oó]n', r'detalle', r'observaci[oó]n', r'nota'],
        'estado': [r'estado', r'status', r'situaci[oó]n'],
    }
    
    def __init__(self):
        self.temp_dir = Config.TEMP_MUESTRAS_DIR
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze_files(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Analiza múltiples archivos Excel y detecta campos comunes
        
        Args:
            file_paths: Lista de rutas a archivos Excel
            
        Returns:
            Diccionario con campos detectados y estadísticas
        """
        all_columns = []
        file_stats = []
        
        for file_path in file_paths:
            try:
                # Leer archivo Excel
                df = pd.read_excel(file_path)
                columns = df.columns.tolist()
                
                all_columns.extend(columns)
                file_stats.append({
                    'file': Path(file_path).name,
                    'columns': columns,
                    'rows': len(df)
                })
            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        # Detectar campos comunes
        detected_fields = self._detect_common_fields(all_columns)
        
        # Calcular estadísticas
        unique_columns = list(set(all_columns))
        column_frequency = {col: all_columns.count(col) for col in unique_columns}
        
        return {
            'detected_fields': detected_fields,
            'statistics': {
                'total_files': len(file_paths),
                'total_columns': len(all_columns),
                'unique_columns': len(unique_columns),
                'files_analyzed': file_stats
            },
            'column_frequency': column_frequency
        }
    
    def _detect_common_fields(self, columns: List[str]) -> List[Dict[str, Any]]:
        """Detecta campos comunes basándose en patrones"""
        detected = []
        
        for column in set(columns):
            col_lower = column.lower()
            
            for field_type, patterns in self.PATRONES.items():
                for pattern in patterns:
                    if re.search(pattern, col_lower):
                        # Determinar tipo de dato
                        data_type = self._infer_data_type(field_type)
                        
                        detected.append({
                            'original_column': column,
                            'suggested_field': field_type,
                            'data_type': data_type,
                            'confidence': self._calculate_confidence(column, pattern),
                            'keywords': [column.lower()]
                        })
                        break
        
        return detected
    
    def _infer_data_type(self, field_type: str) -> str:
        """Infiere el tipo de dato basado en el tipo de campo"""
        type_mapping = {
            'cedula': 'texto',
            'nombre': 'texto',
            'email': 'email',
            'telefono': 'texto',
            'direccion': 'texto',
            'fecha': 'fecha',
            'monto': 'numero',
            'codigo': 'texto',
            'descripcion': 'texto',
            'estado': 'texto'
        }
        return type_mapping.get(field_type, 'texto')
    
    def _calculate_confidence(self, column: str, pattern: str) -> float:
        """Calcula el nivel de confianza de la detección"""
        # Coincidencia exacta = 100%
        if re.fullmatch(pattern, column.lower()):
            return 1.0
        
        # Coincidencia parcial = 70-90%
        if re.search(pattern, column.lower()):
            # Más confianza si el patrón está al inicio
            if re.match(pattern, column.lower()):
                return 0.9
            return 0.7
        
        return 0.5
    
    def create_profile_from_detection(self, 
                                     detected_fields: List[Dict[str, Any]], 
                                     profile_name: str,
                                     profile_description: str = '') -> Dict[str, Any]:
        """Crea un perfil desde los campos detectados"""
        campos = []
        
        for field in detected_fields:
            campos.append({
                'nombre': field['suggested_field'],
                'palabras_clave': field['keywords'],
                'tipo_dato': field['data_type'],
                'requerido': field['confidence'] >= 0.8
            })
        
        return {
            'nombre': profile_name,
            'descripcion': profile_description or f'Perfil generado automáticamente',
            'campos': campos
        }
