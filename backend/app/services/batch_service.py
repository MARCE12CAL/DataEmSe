import pandas as pd
from typing import Dict, Any, List
from pathlib import Path
from config import Config
import json


class BatchService:
    """Servicio para procesamiento por lotes"""
    
    def __init__(self):
        self.batch_jobs_dir = Config.BATCH_JOBS_DIR
        self.batch_jobs_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_batch_script(self, 
                            profile_name: str,
                            csv_path: str,
                            output_folder: str,
                            file_prefix: str = 'procesado') -> str:
        """
        Genera un script Python para procesamiento batch
        
        Args:
            profile_name: Nombre del perfil a usar
            csv_path: Ruta al CSV con configuración
            output_folder: Carpeta donde guardar archivos procesados
            file_prefix: Prefijo para archivos de salida
            
        Returns:
            Script Python como string
        """
        script = f'''#!/usr/bin/env python3
"""
Script de procesamiento batch generado automáticamente
Perfil: {profile_name}
"""

import pandas as pd
from pathlib import Path
import sys

def process_batch():
    """Procesa archivos en lote según configuración"""
    
    # Configuración
    csv_config = "{csv_path}"
    output_folder = Path("{output_folder}")
    file_prefix = "{file_prefix}"
    
    # Crear carpeta de salida
    output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        # Leer configuración
        config_df = pd.read_csv(csv_config)
        
        print(f"Procesando {{len(config_df)}} archivos...")
        
        for idx, row in config_df.iterrows():
            input_file = row.get('input_file')
            
            if pd.isna(input_file) or not Path(input_file).exists():
                print(f"  Archivo no encontrado: {{input_file}}")
                continue
            
            try:
                # Leer archivo Excel
                df = pd.read_excel(input_file)
                
                # Aplicar transformaciones según perfil
                # TODO: Agregar lógica de mapeo del perfil
                
                # Guardar archivo procesado
                output_file = output_folder / f"{{file_prefix}}_{{idx+1}}.xlsx"
                df.to_excel(output_file, index=False)
                
                print(f"✓ Procesado: {{input_file}} -> {{output_file}}")
            
            except Exception as e:
                print(f"✗ Error procesando {{input_file}}: {{e}}")
        
        print("\\n✓ Procesamiento completado")
    
    except Exception as e:
        print(f"✗ Error en procesamiento batch: {{e}}")
        sys.exit(1)

if __name__ == '__main__':
    process_batch()
'''
        return script
    
    def save_batch_job(self, job_name: str, config: Dict[str, Any]) -> str:
        """Guarda configuración de un job batch"""
        job_file = self.batch_jobs_dir / f"{job_name}.json"
        
        with open(job_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return str(job_file)
    
    def get_batch_job(self, job_name: str) -> Dict[str, Any]:
        """Obtiene configuración de un job batch"""
        job_file = self.batch_jobs_dir / f"{job_name}.json"
        
        if not job_file.exists():
            return None
        
        with open(job_file, 'r', encoding='utf-8') as f:
            return json.load(f)
