import pdfplumber

ruta = r"src\pdf\DIFALO0057 CICLON-MC-1-R1.pdf"

with pdfplumber.open(ruta) as pdf:
    p0 = pdf.pages[0]
    # Esto te imprime el ancho y alto total para que te orientes
    print(f"Ancho: {p0.width}, Alto: {p0.height}")
    
    # Prueba con estas coordenadas y ajusta
    im = p0.to_image()
    im.draw_rect((300, 700, 550, 800)) # Dibuja un cuadro rojo en el área
    im.save("debug.png")
