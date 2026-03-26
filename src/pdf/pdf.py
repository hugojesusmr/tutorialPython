import os
import re
import pdfplumber
import pandas as pd

ruta = r"src\pdf"

# ---- PATRONES DE BUSQUEDA ----
p_id_nombre = r'([A-Z]{6}\d{4})\s+(.+)'
p_año = r'\b(20[2-3]\d)\b'
p_prov = r'(?i)(GRUPO\s+[A-Z0-9]+)' 

# --- NORMAS ---
p_norma_rc =  r'(?i)Reglamento de Construcciones.*?(?:Edición|Ed\.)\s*(\d{4})'
p_norma_vcfe = r'(?i)Diseño por Viento.*?C\.F\.E\..*Ed\.(\d{4})'
p_norma_scfe = r'(?i)Diseño por Sismo.*?C\.F\.E\..*Ed\.(\d{4})'

# --- EFICIENCIAS (AJUSTADAS) ---
p_ratio_mastil = r'(?i)M[áa]stil.*?Ratio.*?(\d+(?:\.\d+)?)'
# Se ajustó Monopol.? para capturar "Monopolo" o "Monopolio" y soportar saltos de línea
p_monopolios = r'(?i)Monopol.?\s+Tramo\s+(\d+).*?Ratio.*?(\d+(?:\.\d+)?)'
p_ratio_puntales = r'(?i)Puntales.*?Ratio.*?(\d+(?:\.\d+)?)'
p_desplazamiento = r'(?i)(?:Desplazamiento.*?|δ)\s*[:=]\s*(\d+(?:\.\d+)?)'

def bot_extractor(ruta):
    datos = []
    if not os.path.exists(ruta): return "La carpeta no existe."

    archivos = [f for f in os.listdir(ruta) if f.endswith('.pdf')]
    
    for archivo in archivos:
        ruta_completa = os.path.join(ruta, archivo)
        texto_completo = ""

        with pdfplumber.open(ruta_completa) as pdf:
            for pag in pdf.pages:
                txt = pag.extract_text()
                if txt: texto_completo += txt + "\n"

        if texto_completo:   
            # 1. Extraer Tramos de Monopolio (findall para capturar todos)
            m_tramos = re.findall(p_monopolios, texto_completo)
            # Formato: MT01 45.35
            lista_monopolios = [f"MT{t.zfill(2)} {r}" for t, r in m_tramos]
            val_mono = " | ".join(lista_monopolios) if lista_monopolios else None

            # 2. Otros Ratios
            m_ratio_mastil = re.search(p_ratio_mastil, texto_completo)
            m_ratio_puntales = re.search(p_ratio_puntales, texto_completo)
            m_des = re.search(p_desplazamiento, texto_completo)

            mastil = f"M {m_ratio_mastil.group(1)}" if m_ratio_mastil else None
            puntales = f"P {m_ratio_puntales.group(1)}" if m_ratio_puntales else None
            desplazamiento = f"De {m_des.group(1)}" if m_des else None
            
            # Unir todo lo encontrado
            esfuerzos = " | ".join(filter(None, [val_mono, mastil, puntales, desplazamiento])) or "No encontrado"

            # 3. Normas, ID, etc.
            m_id_nombre = re.search(p_id_nombre, texto_completo)
            m_año = re.search(p_año, texto_completo)
            m_prov = re.search(p_prov, texto_completo)
            m_n_rc = re.search(p_norma_rc, texto_completo)
            m_n_vcfe = re.search(p_norma_vcfe, texto_completo)
            m_n_scfe = re.search(p_norma_scfe, texto_completo)

            normas = []
            if m_n_rc: normas.append(f"RC{m_n_rc.group(1)}")
            if m_n_vcfe: normas.append(f"VCFE{m_n_vcfe.group(1)}")
            if m_n_scfe: normas.append(f"SCFE{m_n_scfe.group(1)}")
            norma_final = " | ".join(normas) if normas else "No encontradas"

            datos.append({
                "AT&T ID": m_id_nombre.group(1) if m_id_nombre else "No encontrado",
                "NOMBRE DE SITIO": m_id_nombre.group(2).strip() if m_id_nombre else "No encontrado",
                "AÑO": m_año.group(0) if m_año else "No encontrado",
                "NORMA": norma_final,
                "EFICIENCIA": esfuerzos,
                "PROVEEDOR": m_prov.group(0) if m_prov else "No encontrado",
            })

    if datos:
        df = pd.DataFrame(datos)
        df.to_excel("extraccion.xlsx", index=False)
        return "Proceso completado."
    return "No se encontraron datos."

print(bot_extractor(ruta))
