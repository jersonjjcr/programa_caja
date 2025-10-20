import subprocess
import re
from typing import List

class ConfiguradorImpresora:
    """Clase para configurar y gestionar impresoras en Windows"""
    
    @staticmethod
    def obtener_impresoras_disponibles() -> List[str]:
        """Obtiene una lista de impresoras disponibles en el sistema"""
        try:
            # Usar PowerShell para obtener impresoras
            cmd = 'powershell "Get-Printer | Select-Object Name"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                impresoras = []
                
                for line in lines[2:]:  # Saltar headers
                    line = line.strip()
                    if line and line != '----':
                        impresoras.append(line)
                
                return impresoras
            else:
                return []
                
        except Exception as e:
            print(f"Error obteniendo impresoras: {e}")
            return []
    
    @staticmethod
    def obtener_impresora_predeterminada() -> str:
        """Obtiene la impresora predeterminada del sistema"""
        try:
            cmd = 'powershell "Get-WmiObject -Query \\"SELECT * FROM Win32_Printer WHERE Default=$true\\" | Select-Object Name"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) >= 3:
                    return lines[2].strip()
            
            return "Impresora predeterminada"
            
        except Exception as e:
            print(f"Error obteniendo impresora predeterminada: {e}")
            return "Impresora predeterminada"
    
    @staticmethod
    def imprimir_archivo_directo(archivo_path: str, impresora: str = None) -> bool:
        """Imprime un archivo directamente usando diferentes métodos"""
        try:
            if impresora:
                # Método 1: copy a LPT1 o puerto de impresora
                if "LPT" in impresora.upper() or "COM" in impresora.upper():
                    cmd = f'copy "{archivo_path}" {impresora}'
                    result = subprocess.run(cmd, shell=True)
                    return result.returncode == 0
                
                # Método 2: print con impresora específica
                cmd = f'print /D:"{impresora}" "{archivo_path}"'
                result = subprocess.run(cmd, shell=True)
                return result.returncode == 0
            else:
                # Método 3: notepad /p para impresora predeterminada
                cmd = f'notepad /p "{archivo_path}"'
                result = subprocess.run(cmd, shell=True)
                return result.returncode == 0
                
        except Exception as e:
            print(f"Error imprimiendo archivo: {e}")
            return False
    
    @staticmethod
    def configurar_impresora_termica():
        """Configuración específica para impresoras térmicas"""
        configuracion = {
            "ancho_papel": 80,  # mm
            "tipo_papel": "continuo",
            "velocidad": "normal",
            "calidad": "draft",
            "codificacion": "cp850"  # Para caracteres especiales
        }
        return configuracion