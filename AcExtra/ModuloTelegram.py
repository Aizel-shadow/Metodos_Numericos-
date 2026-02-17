import logging
import sys
from logging.handlers import RotatingFileHandler
import os
import requests

# --- COLORES Y HANDLER ---

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[36m', 'INFO': '\033[32m', 'WARNING': '\033[33m',
        'ERROR': '\033[31m', 'CRITICAL': '\033[35m\033[1m',
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        original_levelname = record.levelname
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        result = super().format(record)
        record.levelname = original_levelname
        return result

class TelegramHandler(logging.Handler):
    EMOJIS = {'DEBUG': '🔍', 'INFO': 'ℹ️', 'WARNING': '⚠️', 'ERROR': '❌', 'CRITICAL': '🚨'}
    
    def __init__(self, bot_token, chat_id, level=logging.WARNING):
        super().__init__(level)
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self._verificar_conexion()
    
    def _verificar_conexion(self):
        try:
            payload = {'chat_id': self.chat_id, 'text': "✅ Sistema de logging conectado"}
            requests.post(self.url, data=payload, timeout=5)
            print(f"✓ Telegram conectado correctamente")
        except Exception as e:
            print(f"⚠ Error de conexión Telegram: {e}")

    def emit(self, record):
        try:
            log_entry = self.format(record)
            emoji = self.EMOJIS.get(record.levelname, '📝')
            message = f"{emoji} *{record.levelname}*\n\n```\n{log_entry}\n```"
            payload = {'chat_id': self.chat_id, 'text': message, 'parse_mode': 'Markdown'}
            requests.post(self.url, data=payload, timeout=5)
        except Exception:
            pass

# --- CONFIGURACIÓN DEL LOGGER ---

def configurar_logger(nombre='app', nivel_consola=logging.INFO, nivel_archivo=logging.DEBUG, 
                     telegram_token=None, telegram_chat_id=None):
    logger = logging.getLogger(nombre)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        logger.handlers.clear()

    # Consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)-8s | %(message)s', '%H:%M:%S'))
    logger.addHandler(console_handler)

    # Archivo
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler('logs/aplicacion.log', maxBytes=2*1024*1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(file_handler)

    # Telegram (Solo si hay Token e ID)
    if telegram_token and telegram_chat_id:
        t_handler = TelegramHandler(telegram_token, telegram_chat_id, level=logging.ERROR)
        logger.addHandler(t_handler)
    
    return logger

# --- FUNCIONES DE EJEMPLO ---

def simular_error(logger):
    try:
        raise RuntimeError("Error de prueba para Telegram")
    except Exception as e:
        logger.error(f"¡Ocurrió un problema!: {e}")

# --- BLOQUE PRINCIPAL ---

if __name__ == "__main__":
    TOKEN = '8577081025:AAEyM2-mGj4Tzzy4FNjj36F0ser3z4etcfw'
    CHAT_ID = '7164665532'

    print("1. Obtener/Verificar Chat ID")
    print("2. Ejecutar Aplicación (Enviar Errores a Telegram)")
    opcion = input("Elige: ")

    if opcion == "1":
        # Aquí podrías poner la lógica de obtener_chat_id del código original
        print(f"Tu ID configurado es: {CHAT_ID}")
    
    elif opcion == "2":
        # CONFIGURACIÓN ACTIVA
        logger = configurar_logger(
            nombre='metnumbot',
            telegram_token=TOKEN,
            telegram_chat_id=CHAT_ID
        )
        
        logger.info("Iniciando aplicación de prueba...")
        logger.warning("Esto solo se verá en consola.")
        simular_error(logger) # Esto debería llegar a tu Telegram
        logger.info("Fin de la prueba.")