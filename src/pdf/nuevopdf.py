import pdfplumber
import pandas as pd
import re

ruta = r"src\pdf\DIFALO0057 CICLON-MC-1-R1.pdf"

def extraer_tabla_limpia_total(ruta_pdf):
    
    patron = re.compile(r"(\w+)\s+([\d\.,]+\s*mts\.?)\s+([\d\.,]+\s*mts\.?)\s+(\d+)\s*[°º]?\s+(\d+)\s*[°º]?", re.IGNORECASE)
    
    filas_datos = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                # Buscamos todas las coincidencias en el texto de la página
                matches = patron.findall(texto)
                for m in matches:
                    filas_datos.append([str(dato).strip() for dato in m])
                
                if filas_datos: # Si ya encontramos la tabla en esta página, no seguimos
                    break

    if not filas_datos:
        return "No se encontraron datos. Prueba imprimiendo 'print(texto)' para ver cómo lee el PDF."

    columnas_simples = ["SECTOR", "NCRA", "LONG FO", "AZ GEOGRAFICO", "AZ MAGNETICO"]
    df = pd.DataFrame(filas_datos, columns=columnas_simples)

    # --- LIMPIEZA DE DATOS ---
    for col in ["NCRA", "LONG FO"]:
        # Quitamos 'mts', puntos de miles y estandarizamos la coma decimal para Excel latino
        df[col] = df[col].str.replace(r'(?i)mts\.?', '', regex=True).str.strip()
        df[col] = df[col].str.replace('.', ',', regex=False)
        
    nombre_csv = "tabla_datos_limpios.csv"
    
    # Guardar con formato compatible para Excel (punto y coma + BOM)
    df.to_csv(nombre_csv, index=False, sep=';', encoding='utf-8-sig', newline='')
    
    return f"¡Listo! Se encontraron {len(df)} filas. Archivo '{nombre_csv}' generado."

print(extraer_tabla_limpia_total(ruta))
