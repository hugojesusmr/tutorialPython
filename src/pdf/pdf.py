import re
import pdfplumber
import pandas as pd

ruta = r"src\pdf\DIFALO0057 CICLON-MC-1-R1.pdf"

# ---- PATRONES DE BUSQUEDA ----

p_id_nombre = r'([A-Z]{6}\d{4})\s+(.+)'
p_año = r'\b(20[2-3]\d)\b'
p_prov = r'(?i)(GRUPO\s+[A-Z0-9]+)' 

# ---- Normas ----
p_norma_rc =  r'(?i)Reglamento de Construcciones.*?(?:Edición|Ed\.)\s*(\d{4})'
p_norma_vcfe = r'(?i)Diseño por Viento.*?C\.F\.E\..*Ed\.(\d{4})'
p_norma_scfe = r'(?i)Diseño por Sismo.*?C\.F\.E\..*Ed\.(\d{4})'

# ---- Busca Ratio ----
p_ratio_mastil = r'(?i)Ratio.*?(\d+\.?\d*)'

# ---- Busca Desplazamiento ----
p_des = r'(?i)Desplazamiento.*?[:=]\s*(\d+\.?\d*)'

def bot_extractor_excel(ruta):
    
    datos = []
    texto_completo = ""
    
    with pdfplumber.open(ruta) as pdf:

        for pag in pdf.pages:
            txt = pag.extract_text()
            
            if txt:
                texto_completo += txt +"\n"

        if texto_completo:    
            m_id_nombre = re.search(p_id_nombre, texto_completo)
            m_año = re.search(p_año, texto_completo)
            m_prov = re.search(p_prov, texto_completo)
            m_norma_rc = re.search(p_norma_rc, texto_completo)
            m_norma_vcfe = re.search(p_norma_vcfe, texto_completo)
            m_norma_scfe = re.search(p_norma_scfe, texto_completo)
            m_ratio_mastil = re.search(p_ratio_mastil, texto_completo)
            m_des = re.search(p_des, texto_completo)

            id_sitio = m_id_nombre.group(1) if m_id_nombre else "No encotrado"
            nombre_sitio = m_id_nombre.group(2) if m_id_nombre else "No encotrado"
            año = m_año.group(0) if m_año else "No encontrado"
            proveedor = m_prov.group(0) if m_prov else "No encotrado"
            
            mastil = f"M {m_ratio_mastil.group(1)}" if m_ratio_mastil else "No se encontrol"
            eficiencia = f"De {m_des.group(1)}" if m_des else "No se encontrol"
            
            esfuerzos = " | ".join(filter(None, [mastil, eficiencia])) or "No encontrado"
            # ---- Logica de Normas ----
            normas = []
            
            # 1. ---- Reglamento ----
            if m_norma_rc:
                normas.append(f"RC{m_norma_rc.group(1)}")
            # 2. ---- Viento ----
            if m_norma_vcfe:
                normas.append(f"VCFE{m_norma_vcfe.group(1)}")

            # 3. ---- Sismo ----
            if m_norma_scfe:
                normas.append(f"SCFE{m_norma_scfe.group(1)}")

            # 4. ---- Unir normas ----    
            norma = " | ".join(normas) if normas else "No encotradas"

            datos.append({
                "AT&T ID":id_sitio,
                "NOMBRE DE SITIO":nombre_sitio,
                "AÑO": año,
                "NORMA":norma,
                "EFICIENCIA": esfuerzos,
                "PROVEEDOR":proveedor,
            })

        df = pd.DataFrame(datos)
        df.to_excel("extraccion.xlsx", index=False)

bot_extractor_excel(ruta)
