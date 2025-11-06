import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class ScannerService:
    """Servicio para escanear directorios y encontrar archivos Excel"""
    
    EXCEL_EXTENSIONS = ['.xlsx', '.xls', '.xlsm', '.csv']
    
    def scan_folder(self, folder_path: str, recursive: bool = True) -> Dict[str, Any]:
        """
        Escanea una carpeta en busca de archivos Excel
        
        Args:
            folder_path: Ruta de la carpeta a escanear
            recursive: Si debe buscar recursivamente en subcarpetas
            
        Returns:
            Diccionario con archivos encontrados y estadísticas
        """
        folder = Path(folder_path)
        
        if not folder.exists() or not folder.is_dir():
            raise ValueError(f"La carpeta no existe: {folder_path}")
        
        excel_files = []
        
        if recursive:
            # Búsqueda recursiva
            for ext in self.EXCEL_EXTENSIONS:
                excel_files.extend(folder.rglob(f'*{ext}'))
        else:
            # Solo la carpeta principal
            for ext in self.EXCEL_EXTENSIONS:
                excel_files.extend(folder.glob(f'*{ext}'))
        
        # Obtener información de cada archivo
        files_info = []
        total_size = 0
        
        for file_path in excel_files:
            file_stat = file_path.stat()
            file_info = {
                'name': file_path.name,
                'path': str(file_path),
                'size_bytes': file_stat.st_size,
                'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
                'modified': datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                'extension': file_path.suffix
            }
            files_info.append(file_info)
            total_size += file_stat.st_size
        
        return {
            'folder': str(folder),
            'files_found': len(files_info),
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files': sorted(files_info, key=lambda x: x['modified'], reverse=True)
        }
    
    def generate_config_csv(self, files: List[Dict[str, Any]], output_path: str) -> str:
        """
        Genera un CSV de configuración para procesamiento batch
        
        Args:
            files: Lista de archivos encontrados
            output_path: Ruta donde guardar el CSV
            
        Returns:
            Ruta del CSV generado
        """
        import pandas as pd
        
        df = pd.DataFrame([
            {'input_file': f['path'], 'process': True}
            for f in files
        ])
        
        df.to_csv(output_path, index=False)
        return output_path
