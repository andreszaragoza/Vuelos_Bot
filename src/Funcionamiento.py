import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar nuestras clases
from src import SkyscannerBot, NotificadorTelegram
from configuracion import config

def main():
    """Función principal"""
    
    # Verificar API key
    if not config.SKYSCANNER_API_KEY:
        print("❌ Error: SKYSCANNER_API_KEY no configurada")
        return
    
    # Inicializar bot
    bot = SkyscannerBot(config.SKYSCANNER_API_KEY)
    
    # Cargar alertas existentes
    bot.cargar_alertas(config.ARCHIVO_ALERTAS)
    
    # Configurar notificaciones
    notificador = None
    if config.TELEGRAM_TOKEN and config.TELEGRAM_CHAT_ID:
        notificador = NotificadorTelegram(config.TELEGRAM_TOKEN, config.TELEGRAM_CHAT_ID)
        print("✅ Notificaciones por Telegram configuradas")
    
    # Agregar algunas alertas de ejemplo si no hay ninguna
    if not bot.alertas:
        print("📝 Agregando alertas de ejemplo...")
        fecha_ida = datetime.now() + timedelta(days=30)
        fecha_vuelta = fecha_ida + timedelta(days=7)
        
        bot.agregar_alerta("MAD", "BCN", 100, fecha_ida, fecha_vuelta)
        bot.agregar_alerta("MAD", "CDG", 150, fecha_ida, fecha_vuelta)
        
        # Guardar alertas
        os.makedirs('data', exist_ok=True)
        bot.guardar_alertas(config.ARCHIVO_ALERTAS)
    
    # Ejecutar verificación inicial
    print("🚀 Realizando verificación inicial...")
    bot.verificar_alertas()
    
    # Loop principal
    print(f"\n🤖 Bot iniciado. Verificando cada {config.INTERVALO_VERIFICACION_HORAS} horas...")
    print("Presiona Ctrl+C para detener")
    
    try:
        while True:
            time.sleep(config.INTERVALO_VERIFICACION_HORAS * 3600)
            bot.verificar_alertas()
            bot.guardar_alertas(config.ARCHIVO_ALERTAS)
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por el usuario")
        bot.guardar_alertas(config.ARCHIVO_ALERTAS)

if __name__ == "__main__":
    main()