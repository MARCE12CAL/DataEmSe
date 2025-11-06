import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from config import Config
import json


class ExporterService:
    """Servicio para exportar datos a diferentes formatos"""
    
    def __init__(self):
        self.outputs_dir = Config.OUTPUTS_DIR
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_csv(self, file_path: str, output_name: str = None, delimiter: str = ',') -> str:
        """Exporta Excel a CSV"""
        df = pd.read_excel(file_path)
        
        if output_name is None:
            output_name = f"{Path(file_path).stem}.csv"
        
        output_path = self.outputs_dir / output_name
        df.to_csv(output_path, index=False, sep=delimiter)
        
        return str(output_path)
    
    def export_to_json(self, file_path: str, output_name: str = None, orient: str = 'records') -> str:
        """Exporta Excel a JSON"""
        df = pd.read_excel(file_path)
        
        if output_name is None:
            output_name = f"{Path(file_path).stem}.json"
        
        output_path = self.outputs_dir / output_name
        df.to_json(output_path, orient=orient, force_ascii=False, indent=2)
        
        return str(output_path)
    
    def export_to_sql(self, 
                     file_path: str, 
                     table_name: str,
                     database_type: str = 'postgresql',
                     output_name: str = None) -> str:
        """
        Genera script SQL desde Excel
        
        Args:
            file_path: Ruta al archivo Excel
            table_name: Nombre de la tabla en la BD
            database_type: Tipo de base de datos (postgresql, mysql, sqlite)
            output_name: Nombre del archivo SQL de salida
            
        Returns:
            Ruta del archivo SQL generado
        """
        df = pd.read_excel(file_path)
        
        if output_name is None:
            output_name = f"{table_name}.sql"
        
        output_path = self.outputs_dir / output_name
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Generar CREATE TABLE
            f.write(f"-- Tabla: {table_name}\n")
            f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
            
            columns = []
            for col in df.columns:
                # Inferir tipo de dato
                dtype = df[col].dtype
                
                if dtype == 'int64':
                    sql_type = 'INTEGER'
                elif dtype == 'float64':
                    sql_type = 'DECIMAL(10,2)'
                elif dtype == 'datetime64[ns]':
                    sql_type = 'TIMESTAMP'
                else:
                    sql_type = 'VARCHAR(255)'
                
                columns.append(f"    {col} {sql_type}")
            
            f.write(',\n'.join(columns))
            f.write("\n);\n\n")
            
            # Generar INSERTs
            f.write(f"-- Inserts para {table_name}\n")
            
            for idx, row in df.iterrows():
                values = []
                for val in row:
                    if pd.isna(val):
                        values.append('NULL')
                    elif isinstance(val, str):
                        # Escapar comillas simples
                        val_escaped = val.replace("'", "''")
                        values.append(f"'{val_escaped}'")
                    else:
                        values.append(str(val))
                
                insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(values)});\n"
                f.write(insert_sql)
        
        return str(output_path)
    
    def export_multiple_formats(self, 
                               file_path: str, 
                               formats: List[str] = ['csv', 'json']) -> Dict[str, str]:
        """Exporta a múltiples formatos"""
        results = {}
        
        if 'csv' in formats:
            try:
                results['csv'] = self.export_to_csv(file_path)
            except Exception as e:
                results['csv_error'] = str(e)
        
        if 'json' in formats:
            try:
                results['json'] = self.export_to_json(file_path)
            except Exception as e:
                results['json_error'] = str(e)
        
        if 'sql' in formats:
            try:
                table_name = Path(file_path).stem.replace('-', '_').replace(' ', '_')
                results['sql'] = self.export_to_sql(file_path, table_name)
            except Exception as e:
                results['sql_error'] = str(e)
        
        return results
