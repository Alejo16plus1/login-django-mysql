import imgkit
config = imgkit.config(wkhtmltoimage='C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')

def tomar_captura(url, output_path):
    imgkit.from_url(url, output_path)
    print(f"Captura guardada en: {output_path}")

# Probar con una URL
tomar_captura("https://google.com", "captura.jpg")
