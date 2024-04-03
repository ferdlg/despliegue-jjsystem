import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario, asunto, estado):
    load_dotenv()

    remitente = os.getenv('USER')
    password = os.getenv('PASS')

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Lee el contenido del template HTML
    with open('templates/estado_envio.html', 'r') as archivo:
        template_html = archivo.read()

    # Renderiza el template con el estado actualizado
    mensaje = template_html.replace('{{ estado }}', estado)

    # Adjunta el mensaje al correo
    msg.attach(MIMEText(mensaje, 'html'))

    # Establece la conexión SMTP y envía el correo
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, password)
    text = msg.as_string()
    server.sendmail(remitente, destinatario, text)
    server.quit()
