env_content = """# API Keys
SKYSCANNER_API_KEY=tu_api_key_de_skyscanner_aqui

# Telegram (opcional)
TELEGRAM_TOKEN=tu_token_de_telegram_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui

# Email (opcional)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_ADDRESS=tu_email@gmail.com
EMAIL_PASSWORD=tu_password_de_aplicacion
EMAIL_DESTINATARIO=destinatario@gmail.com

# Configuración del bot
INTERVALO_HORAS=2
ARCHIVO_ALERTAS=data/alertas.json
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("✅ Archivo .env creado")
print("📝 IMPORTANTE: Debes editar este archivo y poner tus API keys reales")