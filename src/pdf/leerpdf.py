import pdfplumber
import pandas as pd
import re

ruta = r"src\pdf\TLAIMM0415-R&R-POPOCATLA.pdf"
def extraer_tabla_limpia_total(ruta_pdf):
    patron = re.compile(r"(\w+)\s+([\d\.]+\s*mts\.)\s+([\d\.]+\s*mts\.)\s+(\d+°)\s+(\d+°)")
    
    filas_datos = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                matches = patron.findall(texto)
                if matches:
                    # Guardamos las filas encontradas como listas de texto limpio
                    for m in matches:
                        filas_datos.append([str(dato).strip() for dato in m])
                    break # Solo la primera tabla detectada

    if not filas_datos:
        return "No se encontraron datos en el PDF."

    # --- NOMBRES DE COLUMNA SIN ACENTOS NI CARACTERES RAROS ---
    columnas_simples = ["SECTOR", "NCRA", "LONG FO", "AZ GEOGRAFICO", "AZ MAGNETICO"]
    
    df = pd.DataFrame(filas_datos, columns=columnas_simples)

    # --- FORMATO LATINO (Coma decimal y limpieza de unidades) ---
    # Columnas de distancia
    for col in ["NCRA", "LONG FO"]:
        df[col] = df[col].str.replace('mts.', '', regex=False).str.strip().astype(float)
        
    # Columnas de angulos (quitamos el símbolo de grado)
    for col in ["AZ GEOGRAFICO", "AZ MAGNETICO"]:
        df[col] = df[col].str.replace('°', '', regex=False).str.strip()

    # --- GUARDAR SIN FILAS VACÍAS Y COMPATIBLE CON EXCEL ---
    nombre_csv = "tabla_datos_limpios.csv"
    
    # newline='' evita filas vacías en Windows
    with open(nombre_csv, 'w', encoding='utf-8-sig', newline='') as f:
        # Instrucción para que Excel separe por columnas automáticamente
        f.write("sep=;\n")
        df.to_csv(f, index=False, sep=';')
    
    return f"¡Listo! Archivo '{nombre_csv}' generado con éxito."

# --- EJECUCIÓN ---
print(extraer_tabla_limpia_total(ruta))




           
