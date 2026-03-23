import os
import re
import pdfplumber
import pandas as pd

ruta = r"src\pdf"

# ---- PATRONES DE BUSQUEDA ----
p_id_nombre = r'([A-Z]{6}\d{4})\s+(.+)'
p_año = r'\b(20[2-3]\d)\b'
p_prov = r'(?i)(GRUPO\s+[A-Z0-9]+)' 

# ---- Normas ----
p_norma_rc =  r'(?i)Reglamento de Construcciones.*?(?:Edición|Ed\.)\s*(\d{4})'
p_norma_vcfe = r'(?i)Diseño por Viento.*?C\.F\.E\..*Ed\.(\d{4})'
p_norma_scfe = r'(?i)Diseño por Sismo.*?C\.F\.E\..*Ed\.(\d{4})'

# ---- Eficiencia ----
p_ratio_mastil = r'(?i)M[áa]stil.*?Ratio.*?(\d+(?:\.\d+)?)'
p_ratio_puntales = r'(?i)Puntales.*?Ratio.*?(\d+(?:\.\d+)?)'
p_desplazamiento = r'(?i)(?:Desplazamiento.*?|δ)\s*[:=]\s*(\d+(?:\.\d+)?)'

def bot_extractor(ruta):
    datos = []
    if not os.path.exists(ruta):
        return "La carpeta no existe."

    archivos = [f for f in os.listdir(ruta) if f.endswith('.pdf')]
    
    for archivo in archivos:
        ruta_completa = os.path.join(ruta, archivo)
        texto_completo = ""

        with pdfplumber.open(ruta_completa) as pdf:
            for pag in pdf.pages:
                txt = pag.extract_text()
                if txt:
                    texto_completo += txt + "\n"

        if texto_completo:    
            m_id_nombre = re.search(p_id_nombre, texto_completo)
            m_año = re.search(p_año, texto_completo)
            m_prov = re.search(p_prov, texto_completo)
            m_norma_rc = re.search(p_norma_rc, texto_completo)
            m_norma_vcfe = re.search(p_norma_vcfe, texto_completo)
            m_norma_scfe = re.search(p_norma_scfe, texto_completo)
            m_ratio_mastil = re.search(p_ratio_mastil, texto_completo)
            m_ratio_puntales = re.search(p_ratio_puntales, texto_completo)
            m_des = re.search(p_desplazamiento, texto_completo)

            # --- Formateo de Eficiencia (Cambiado para que filter funcione) ---
            # Usamos None si no existe para que no ensucie el "|"
            mastil = f"M {m_ratio_mastil.group(1)}" if m_ratio_mastil else None
            puntales = f"P {m_ratio_puntales.group(1)}" if m_ratio_puntales else None
            desplazamiento = f"De {m_des.group(1)}" if m_des else None
            
            esfuerzos = " | ".join(filter(None, [mastil, puntales, desplazamiento])) or "No encontrado"

            # ---- Lógica de Normas ----
            normas = []
            if m_norma_rc: normas.append(f"RC{m_norma_rc.group(1)}")
            if m_norma_vcfe: normas.append(f"VCFE{m_norma_vcfe.group(1)}")
            if m_norma_scfe: normas.append(f"SCFE{m_norma_scfe.group(1)}")
            norma_final = " | ".join(normas) if normas else "No encontradas"

            datos.append({
                "AT&T ID": m_id_nombre.group(1) if m_id_nombre else "No encontrado",
                "NOMBRE DE SITIO": m_id_nombre.group(2).strip() if m_id_nombre else "No encontrado",
                "AÑO": m_año.group(0) if m_año else "No encontrado",
                "NORMA": norma_final,
                "EFICIENCIA": esfuerzos,
                "PROVEEDOR": m_prov.group(0) if m_prov else "No encontrado",
            })

    # --- GUARDAR FUERA DEL BUCLE ---
    if datos:
        df = pd.DataFrame(datos)
        df.to_excel("extraccion.xlsx", index=False)
        return "Proceso completado. Excel generado."
    else:
        return "No se encontraron datos en los archivos."

print(bot_extractor(ruta))
