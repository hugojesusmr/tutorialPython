import re
import os
import pdfplumber
import pandas as pd

ruta_carpeta = r"src\pdf"
p_id_nombre = r'([A-Z]{6}\d{4})\s+(.+)'

def bot_extractor_masivo(ruta_entrada):
    datos_totales = [] 
    
    if not os.path.exists(ruta_entrada): return "La Carpeta No Existe."
    archivos = [f for f in os.listdir(ruta_entrada) if f.endswith('.pdf')]

    for archivo in archivos:
        ruta_pdf = os.path.join(ruta_entrada, archivo)
        id_sitio, nombre_sitio = "No encontrado", "No encontrado"

        with pdfplumber.open(ruta_pdf) as pdf:
            # 1. Extraer ID y Nombre
            texto_p1 = pdf.pages[0].extract_text()
            match = re.search(p_id_nombre, texto_p1 or "")
            if match:
                id_sitio, nombre_sitio = match.group(1), match.group(2).strip()

            area_recortada = None
            for num_pag, pagina in enumerate(pdf.pages):
                busqueda = pagina.search("ACCESORIOS Y ANTENAS")
                if busqueda:
                    posicion_y = busqueda[0]['top']
                    limite_inferior = min(posicion_y + 500, pagina.height)
                    area_recortada = pagina.within_bbox((0, posicion_y, pagina.width, limite_inferior))
                    break 
            
            if not area_recortada: continue 

            # Reducimos x_tolerance para evitar que se peguen los números
            settings = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text",
                "snap_y_tolerance": 4,
                "intersection_x_tolerance": 10 
            }
            
            tabla = area_recortada.extract_table(table_settings=settings)
            
            if tabla:
                tipos_validos = ["Existente", "Adicional", "Futuro", "Sustitución"]
                p_tipo = r'(' + '|'.join(tipos_validos) + r')'

                for fila in tabla:
                    # Limpieza inicial de la fila
                    f = [str(c).strip() for c in fila if c]
                    texto_fila = " ".join(f)
                    
                    # 1. BUSCAMOS LA ALTURA
                    m_altura = re.search(r'\d+\.\d+', texto_fila)
                    if not m_altura: continue
                    altura_val = m_altura.group(0)

                    # 2. BUSCAMOS EL TIPO
                    m_tipo = re.search(p_tipo, texto_fila, re.IGNORECASE)
                    if not m_tipo: continue
                    tipo_val = m_tipo.group(1)

                    # --- 3. LÓGICA DE CANTIDAD (SÚPER REFORZADA) ---
                    # Extraemos todos los números enteros de la fila
                    enteros = re.findall(r'\b\d+\b', texto_fila)
                    
                    # FILTRO DE RUIDO:
                    # Si la fila empieza con T1, T2, etc., el primer número es el tramo. Lo quitamos.
                    if re.match(r'^T\d+', texto_fila) and len(enteros) > 0:
                        enteros.pop(0)
                    
                    # Quitamos números que coincidan con la parte entera de la altura
                    parte_entera_altura = altura_val.split('.')[0]
                    enteros = [n for n in enteros if n != parte_entera_altura]

                    cantidad = ""
                    
                    # Buscamos la relación Peso * Cantidad = Total de atrás hacia adelante
                    # La terna suele ser la última de la fila (o penúltima si hay 'Peso/tramo')
                    if len(enteros) >= 3:
                        # Revisamos las ternas desde el final
                        for i in range(len(enteros) - 2):
                            v1, v2, v3 = int(enteros[i]), int(enteros[i+1]), int(enteros[i+2])
                            if v1 * v2 == v3 and v2 > 0:
                                cantidad = str(v2)
                                break
                    
                    # Fallback 1: Si no hubo match matemático, tomamos el penúltimo número
                    # (En casi todas tus tablas la Cantidad es el penúltimo antes del Total)
                    if not cantidad and len(enteros) >= 2:
                        # Si hay un 'Peso/tramo' al final, la cantidad sería enteros[-3]
                        # Si no hay 'Peso/tramo', es enteros[-2]
                        # Como la cantidad suele ser pequeña (<50), usamos eso de filtro
                        for n in reversed(enteros[:-1]):
                            if int(n) < 50:
                                cantidad = n
                                break

                    # Si sigue vacío, por defecto 1
                    if not cantidad: cantidad = "1"

                                      # 4. LIMPIEZA DE NOMBRE (REFORZADA PARA NÚMEROS EN EL NOMBRE)
                    try:
                        # Extraemos la parte de la fila que está después del TIPO
                        parte_nombre_peso = texto_fila.split(tipo_val)[-1].strip()
                        
                        # Buscamos el PESO: es el primer número entero después del nombre.
                        # El nombre termina donde empieza el patrón: Espacio + Número + Espacio + Cantidad
                        # O simplemente buscamos el peso que precede a la multiplicación exitosa.
                        
                        # Usamos una expresión que captura el texto hasta encontrarse con 
                        # los números de Peso, Cantidad y Total al final.
                        m_detalles = re.search(r'^(.*?)\s+(\d+)\s+(\d+)\s+(\d+\.?\d*)', parte_nombre_peso)
                        
                        if m_detalles:
                            nombre_final = m_detalles.group(1).strip()
                            # Opcional: si quieres asegurar que no se traiga la altura de equipo
                            nombre_final = nombre_final.replace(altura_val, "").strip()
                        else:
                            # Fallback si la estructura varía:
                            nombre_final = parte_nombre_peso.split(altura_val)[-1].strip()
                            
                    except:
                        nombre_final = "No detectado"



                    datos_totales.append({
                        "ID SITIO": id_sitio,
                        "NOMBRE SITIO": nombre_sitio,
                        "ALTURA": altura_val,
                        "TIPO": tipo_val,
                        "NOMBRE": nombre_final,
                        "CANTIDAD": cantidad
                    })

    if datos_totales:
        df = pd.DataFrame(datos_totales)
        df.to_excel("Resultado_Final_Corregido.xlsx", index=False)
        return f"¡Éxito! Se procesaron {len(df)} filas."
    
    return "No se encontraron datos."

print(bot_extractor_masivo(ruta_carpeta))
