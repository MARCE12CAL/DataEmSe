import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from config import Config
import json
from datetime import datetime


class ComparatorService:
    """Servicio para comparar archivos Excel contra un modelo/perfil"""
    
    def __init__(self):
        self.reports_dir = Config.COMPARISON_REPORTS_DIR
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def compare_with_model(self, 
                          file_path: str, 
                          model_columns: List[str]) -> Dict[str, Any]:
        """
        Compara un archivo Excel contra un modelo de columnas esperadas
        
        Args:
            file_path: Ruta al archivo Excel a comparar
            model_columns: Lista de columnas esperadas según el modelo
            
        Returns:
            Diccionario con resultados de la comparación
        """
        try:
            df = pd.read_excel(file_path)
            file_columns = df.columns.tolist()
            
            # Normalizar nombres para comparación
            model_norm = [col.strip().lower() for col in model_columns]
            file_norm = [col.strip().lower() for col in file_columns]
            
            # Columnas faltantes
            missing_columns = [col for col in model_norm if col not in file_norm]
            
            # Columnas adicionales
            extra_columns = [col for col in file_norm if col not in model_norm]
            
            # Columnas coincidentes
            matching_columns = [col for col in file_norm if col in model_norm]
            
            # Calcular porcentaje de similitud
            similarity = (len(matching_columns) / len(model_columns) * 100) if model_columns else 0
            
            # Analizar tipos de datos
            data_type_issues = self._check_data_types(df, matching_columns)
            
            # Verificar datos faltantes
            missing_data = self._check_missing_data(df)
            
            comparison = {
                'file': Path(file_path).name,
                'timestamp': datetime.now().isoformat(),
                'similarity_percentage': round(similarity, 2),
                'total_model_columns': len(model_columns),
                'total_file_columns': len(file_columns),
                'matching_columns': matching_columns,
                'missing_columns': missing_columns,
                'extra_columns': extra_columns,
                'data_type_issues': data_type_issues,
                'missing_data': missing_data,
                'status': 'completo' if similarity >= 90 else 'incompleto'
            }
            
            # Guardar reporte
            report_name = f"comparison_{Path(file_path).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_path = self.reports_dir / report_name
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(comparison, f, ensure_ascii=False, indent=2)
            
            comparison['report_path'] = str(report_path)
            
            return comparison
        
        except Exception as e:
            raise Exception(f"Error comparing file: {str(e)}")
    
    def _check_data_types(self, df: pd.DataFrame, columns: List[str]) -> List[Dict[str, Any]]:
        """Verifica tipos de datos de las columnas"""
        issues = []
        
        for col in columns:
            if col in df.columns:
                dtype = str(df[col].dtype)
                
                # Detectar problemas potenciales
                if df[col].isnull().any():
                    null_count = df[col].isnull().sum()
                    issues.append({
                        'column': col,
                        'issue': 'missing_values',
                        'count': int(null_count),
                        'percentage': round(null_count / len(df) * 100, 2)
                    })
        
        return issues
    
    def _check_missing_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Verifica datos faltantes en el archivo"""
        total_cells = df.size
        missing_cells = df.isnull().sum().sum()
        
        return {
            'total_cells': int(total_cells),
            'missing_cells': int(missing_cells),
            'missing_percentage': round(missing_cells / total_cells * 100, 2) if total_cells > 0 else 0
        }
    
    def get_comparison_report(self, report_name: str) -> Dict[str, Any]:
        """Obtiene un reporte de comparación guardado"""
        report_path = self.reports_dir / report_name
        
        if not report_path.exists():
            return None
        
        with open(report_path, 'r', encoding='utf-8') as f:
            return json.load(f)
