import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import requests

class NotificadorEmail:
    """Notificador por email"""
    
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
    
    def enviar_oferta(self, vuelo: Dict, destinatario: str):
        """Enviar notificación de oferta por email"""
        
        mensaje = MIMEMultipart()
        mensaje['From'] = self.email
        mensaje['To'] = destinatario
        mensaje['Subject'] = f"🎉 Oferta de vuelo: {vuelo['origen']} → {vuelo['destino']}"
        
        cuerpo = f"""
        ¡Hola! He encontrado una oferta de vuelo:
        
        ✈️ Ruta: {vuelo['origen']} → {vuelo['destino']}
        💰 Precio: {vuelo['precio']}€
        📅 Fecha ida: {vuelo['fecha_ida']}
        📅 Fecha vuelta: {vuelo['fecha_vuelta'] or 'Solo ida'}
        
        ¡No dejes pasar esta oportunidad!
        """
        
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(mensaje)
            server.quit()
            print(f"✅ Email enviado a {destinatario}")
        except Exception as e:
            print(f"❌ Error enviando email: {e}")

class NotificadorTelegram:
    """Notificador por Telegram"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    def enviar_oferta(self, vuelo: Dict):
        """Enviar notificación de oferta por Telegram"""
        
        mensaje = f"""
🎉 *¡OFERTA ENCONTRADA!* 🎉
✈️ {vuelo['origen']} → {vuelo['destino']}
💰 *Precio: {vuelo['precio']}€*
📅 Ida: {vuelo['fecha_ida']}
📅 Vuelta: {vuelo['fecha_vuelta'] or 'Solo ida'}
        """
        
        data = {
            'chat_id': self.chat_id,
            'text': mensaje,
            'parse_mode': 'Markdown'
        }
        
        try:
            response = requests.post(self.url, data=data)
            if response.status_code == 200:
                print("✅ Mensaje enviado por Telegram")
            else:
                print(f"❌ Error enviando Telegram: {response.status_code}")
        except Exception as e:
            print(f"❌ Error enviando Telegram: {e}")