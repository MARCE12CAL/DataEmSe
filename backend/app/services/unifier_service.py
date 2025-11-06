import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from config import Config


class UnifierService:
    """Servicio para unificar múltiples archivos Excel en uno solo"""
    
    def __init__(self):
        self.outputs_dir = Config.OUTPUTS_DIR
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def unify_files(self, 
                   file_paths: List[str], 
                   output_name: str = 'unificado.xlsx',
                   remove_duplicates: bool = False,
                   add_source_column: bool = True) -> Dict[str, Any]:
        """
        Unifica múltiples archivos Excel en uno solo
        
        Args:
            file_paths: Lista de rutas a archivos Excel
            output_name: Nombre del archivo de salida
            remove_duplicates: Si debe eliminar filas duplicadas
            add_source_column: Si debe agregar columna con el archivo origen
            
        Returns:
            Diccionario con información del proceso
        """
        all_data = []
        
        for file_path in file_paths:
            try:
                df = pd.read_excel(file_path)
                
                if add_source_column:
                    df['archivo_origen'] = Path(file_path).name
                
                all_data.append(df)
            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
        
        if not all_data:
            raise ValueError("No se pudieron leer archivos")
        
        # Combinar todos los DataFrames
        unified_df = pd.concat(all_data, ignore_index=True)
        
        # Homologar nombres de columnas (opcional)
        unified_df.columns = [col.strip().lower().replace(' ', '_') for col in unified_df.columns]
        
        # Eliminar duplicados si se solicita
        if remove_duplicates:
            before_count = len(unified_df)
            unified_df = unified_df.drop_duplicates()
            after_count = len(unified_df)
            duplicates_removed = before_count - after_count
        else:
            duplicates_removed = 0
        
        # Guardar archivo unificado
        output_path = self.outputs_dir / output_name
        unified_df.to_excel(output_path, index=False)
        
        return {
            'output_file': str(output_path),
            'total_rows': len(unified_df),
            'total_columns': len(unified_df.columns),
            'files_processed': len(file_paths),
            'duplicates_removed': duplicates_removed,
            'columns': unified_df.columns.tolist()
        }
    
    def normalize_column_names(self, file_path: str) -> Dict[str, str]:
        """Normaliza nombres de columnas de un archivo"""
        df = pd.read_excel(file_path)
        
        original_columns = df.columns.tolist()
        normalized_columns = [col.strip().lower().replace(' ', '_') for col in original_columns]
        
        return dict(zip(original_columns, normalized_columns))
