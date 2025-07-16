import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuración del bot"""
    
    # API Keys
    SKYSCANNER_API_KEY: str = os.getenv('SKYSCANNER_API_KEY', '')
    
    # Telegram
    TELEGRAM_TOKEN: Optional[str] = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv('TELEGRAM_CHAT_ID')
    
    # Email
    EMAIL_SMTP_SERVER: str = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
    EMAIL_SMTP_PORT: int = int(os.getenv('EMAIL_SMTP_PORT', '587'))
    EMAIL_ADDRESS: Optional[str] = os.getenv('EMAIL_ADDRESS')
    EMAIL_PASSWORD: Optional[str] = os.getenv('EMAIL_PASSWORD')
    EMAIL_DESTINATARIO: Optional[str] = os.getenv('EMAIL_DESTINATARIO')
    
    # Bot settings
    INTERVALO_VERIFICACION_HORAS: int = int(os.getenv('INTERVALO_HORAS', '2'))
    ARCHIVO_ALERTAS: str = os.getenv('ARCHIVO_ALERTAS', 'data/alertas.json')

# Instancia global de configuración
config = Config()