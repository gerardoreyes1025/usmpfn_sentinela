import subprocess
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import psutil
import os
from ping3 import ping as ping3_ping
import env_utils

# ==============================
# CONFIGURACIÓN DE LOG
# ==============================
# Ruta absoluta solicitada para el archivo de log
LOG_FILE = r"C:\SentryLogs\sentinela_log_redes.txt" 

def registrar_log(mensaje):
    """Guarda en el log solo errores o eventos relevantes en la ruta C:\SentryLogs."""
    try:
        # Asegura que la carpeta exista antes de intentar escribir el archivo
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except Exception as e:
        # Si falla el log, al menos lo imprimimos en consola
        print(f"❌ Error al escribir en el log {LOG_FILE}: {e}")


# ==============================
# CONFIGURACIÓN GENERAL
# ==============================
def obtener_ip_eth172():
    """Devuelve la primera IP local que empiece con 172.19.1."""
    for nombre, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            # addr.family == 2 corresponde a AF_INET (IPv4)
            if addr.family == 2 and addr.address.startswith("172.19.1."):
                return addr.address
    return None

ETH2_IP = obtener_ip_eth172()
if not ETH2_IP:
    print("⚠️ No se encontró ninguna interfaz con IP 172.19.1.x")
    registrar_log("⚠️ No se encontró ninguna interfaz con IP 172.19.1.x. Terminando script.")
    exit(1)
else:
    print(f"✅ IP detectada automáticamente: {ETH2_IP}")
    registrar_log(f"✅ IP detectada automáticamente: {ETH2_IP}")


# Destinos por PING (Lista de Switches)
PING_DESTINOS = {
    "SWITCH_CORE": "172.19.1.254",
    "SWITCH_INFORMATICA_PISO1_1": "172.19.1.3",
    "SWITCH_INFORMATICA_PISO1_2": "172.19.1.4",
    # "SWITCH_INFORMATICA_PISO2_1": "172.19.1.5",
    # "SWITCH_INFORMATICA_PISO2_2": "172.19.1.6",
    #"SWITCH_INFORMATICA_PISO3_1": "172.19.1.8",
    # "SWITCH_INFORMATICA_PISO3_2": "172.19.1.9",
    "SWITCH_GOBIERNO": "172.19.1.31",
    "SWITCH_BIBLIOTECA": "172.19.1.14",
    "SWITCH_RECTORADO": "172.19.1.17",
    #"SWITCH_PABA_PISO1_1":"172.19.1.12",
    "SWITCH_PABA_PISO2_1":"172.19.1.13",
    "SWITCH_PABA_PISO2_2":"172.19.1.30",
    "SWITCH_PABB_PISO1":"172.19.1.25",
    "SWITCH_PABB_PISO2":"172.19.1.26",
    "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED":"172.19.1.16",
    "SWITCH_CIENCIASDELASALUD_PISO2_1":"172.19.1.19",
    "SWITCH_CIENCIASDELASALUD_PISO2_2":"172.19.1.27",
    "SWITCH_CIENCIASDELASALUD_PISO2_3":"172.19.1.29",
    "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED":"172.19.1.28",
    "SWITCH_FIA_PISO1_1":"172.19.1.253",
    "SWITCH_FIA_PISO1_2":"172.19.1.33",
    # "SWITCH_FIA_PISO1_3_TALLERES":"172.19.15.47",
    # "SWITCH_FIA_PISO2_1":"172.19.15.43",
    "SWITCH_FIA_PISO3_1":"172.19.1.43", #210
    # "SWITCH_FIA_PISO3_2":"172.19.15.46"
}

# No se requieren destinos HTTP para el monitoreo de switches
HTTP_DESTINOS = {}

INTERVALO = 60  # segundos (frecuencia con la que se ejecutan las verificaciones)

# --- UMBRALES DE ALERTA ---
CONSECUTIVE_FAILURE_THRESHOLD = 15 # Fallos consecutivos antes de la ALERTA INICIAL de persistencia
INTERMITTENCY_FAILURE_THRESHOLD = 10 # Eventos de caída (OK -> FAIL) antes de la ALERTA INICIAL de inestabilidad


# Tiempos de alerta
# Secuencia de intervalos para Telegram (en minutos): 5m, 15m, 1h, 3h, 6h
INTERVALOS_TELEGRAM_MIN = [5, 15, 60, 180, 360]
# Intervalo fijo para Email (en horas)
INTERVALO_EMAIL_H = 3

env_utils.load_dotenv()

# Telegram y Email desde .env para el script de switches
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_SW", os.getenv("TELEGRAM_TOKEN", ""))
CHAT_ID = int(os.getenv("CHAT_ID_SW", os.getenv("CHAT_ID", "-5038342805")))

EMAIL_FROM = os.getenv("EMAIL_FROM", "gramosr@usmp.pe")
EMAIL_TO = [e.strip() for e in os.getenv("EMAIL_TO_SW", os.getenv("EMAIL_TO", EMAIL_FROM)).split(",") if e.strip()]
EMAIL_PASS = os.getenv("EMAIL_PASS", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


# ==============================
# FUNCIONES DE UTILIDAD
# ==============================

def escape_html(text):
    """Escapa caracteres HTML especiales para que no rompan el parse_mode='HTML' de Telegram."""
    if not isinstance(text, str):
        text = str(text)
    # Reemplaza '&', '<', y '>' con sus entidades HTML correspondientes
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        # Intentamos enviar el mensaje
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}, timeout=10)
        
        # Verificamos la respuesta de la API de Telegram
        if response.status_code == 200 and response.json().get('ok'):
            registrar_log("📲 Notificación de Telegram (SWITCHES) enviada exitosamente.")
            print("📲 Notificación enviada a Telegram (SWITCHES).")
        else:
            error_msg = response.json().get('description', 'Error desconocido en la respuesta de Telegram.')
            registrar_log(f"❌ Error al enviar Telegram (SWITCHES) (Status {response.status_code}): {error_msg}")
            print(f"❌ Error al enviar Telegram (SWITCHES): {error_msg}")
            # Lanzar una excepción para que el manejo de alertas pueda actuar si falla
            raise Exception(f"Fallo en API Telegram (SWITCHES): {error_msg}")
            
    except requests.exceptions.Timeout:
        registrar_log("❌ Error Telegram (SWITCHES): Timeout al conectar con la API.")
        print("❌ Error Telegram (SWITCHES): Timeout al conectar con la API.")
    except requests.exceptions.ConnectionError:
        registrar_log("❌ Error Telegram (SWITCHES): Fallo de conexión (DNS, red, etc.).")
        print("❌ Error Telegram (SWITCHES): Fallo de conexión (DNS, red, etc.).")
    except Exception as e:
        # Capturamos la excepción general, incluyendo la que lanzamos arriba
        registrar_log(f"❌ Error Telegram (SWITCHES): {e}")
        print(f"❌ Error Telegram (SWITCHES): {e}")


def enviar_email(asunto, mensaje):
    msg = MIMEText(mensaje, "html")
    msg["Subject"] = asunto
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        registrar_log("📧 Correo electrónico (SWITCHES) enviado exitosamente.")
        print("📧 Correo enviado correctamente (SWITCHES).")
    except smtplib.SMTPAuthenticationError:
        registrar_log("❌ Error correo (SWITCHES): Fallo de autenticación SMTP (usuario/contraseña incorrectos).")
        print("❌ Error correo (SWITCHES): Fallo de autenticación SMTP (usuario/contraseña incorrectos).")
    except Exception as e:
        registrar_log(f"❌ Error correo (SWITCHES): {e}")
        print(f"❌ Error correo (SWITCHES): {e}")
        # Lanzar una excepción si falla el envío
        raise Exception(f"Fallo al enviar Email (SWITCHES): {e}")


def ping(ip_origen, destino):
    """Devuelve (True, latencia_ms) si responde; (False, None) si no."""
    try:
        # El timeout puede ser ajustado a 1 segundo para la red local, si se desea más rapidez.
        lat = ping3_ping(destino, src_addr=ip_origen, timeout=2, unit='ms') 

        if lat is None or lat is False or lat <= 0 or isinstance(lat, bool):
            return False, None

        return True, int(lat)

    except PermissionError:
        registrar_log(f"❌ Permisos insuficientes para ICMP.")
        return False, None

    except Exception as e:
        registrar_log(f"❌ Excepción en ping a {destino}: {e}")
        return False, None

# Ya no necesitamos check_http()

def diagnosticar(resultados_ping):
    """Evalúa el estado general de conectividad de los switches."""
    total_destinos = len(resultados_ping)
    fallos = sum(1 for ok in resultados_ping.values() if not ok)
    
    if fallos == total_destinos:
        return "FALLO TOTAL EN SWITCHES"
    elif fallos > 0:
        return f"FALLO PARCIAL EN {fallos}/{total_destinos} SWITCHES"
    else:
        return "TODO OK" 

def generar_mensaje_alerta(timestamp, diagnostico, motivo_alerta, resultados_ping, PING_DESTINOS):
    """Genera el cuerpo del mensaje para Telegram y Email (solo PING)."""
    
    if "INESTABILIDAD" in motivo_alerta:
        emoji_principal = "⚡"
    elif "RESTABLECIMIENTO" in motivo_alerta:
        emoji_principal = "✅"
    else:
        emoji_principal = "⚠️"
        
    mensaje = f"<b>{emoji_principal} ALERTA SENTINELA SWITCHES {emoji_principal}</b>\n"
    mensaje += f"Hora: {timestamp}\n"
    mensaje += f"Motivo: <b>{motivo_alerta}</b>\n"
    mensaje += f"Diagnóstico: <b>{diagnostico}</b>\n\n" # Incluimos el diagnóstico resumido aquí
    
    mensaje += "<b>🔹 Resultados PING:</b>\n"
    for nombre, ip in PING_DESTINOS.items():
        ok = resultados_ping.get(nombre, False)
        estado = "✅" if ok else "❌"
        mensaje += f"{estado} {nombre} ({ip})\n"

    # Se omite por completo la sección HTTP
            
    return mensaje


# ==============================
# LOOP PRINCIPAL
# ==============================
def main():
    
    # --- Variables de control de tiempo y alerta ---
    ultima_alerta = {
        "telegram": datetime.min,
        "email": datetime.min
    }
    
    # --- Variables de estado de monitoreo ---
    estado_anterior = {nombre: None for nombre in PING_DESTINOS}
    fallos_consecutivos = {nombre: 0 for nombre in PING_DESTINOS}
    
    # --- Variables de estado de ALERTA ---
    drop_events_count = 0      # Contador de veces que el sistema pasa de OK a FALLO. Se resetea al enviar RESTABLECIMIENTO.
    initial_alert_sent = False # Indica si ya se envió la primera alerta (por persistencia o intermitencia).
    was_failing = False        # ¿Estaba fallando en la iteración ANTERIOR?
    
    # Intervalos secuenciales de Telegram en minutos
    INTERVALOS_TELEGRAM_MIN = [5, 15, 60, 180, 360] 
    indice_intervalo_telegram = 0
    
    registrar_log("--- Sentinela de Switches iniciado. ---")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ahora = datetime.now()

        resultados_ping = {}
        # resultados_http ya no es necesaria

        print(f"\n🕒 Verificación de Switches: {timestamp}")

        # --- Verificación PING y registro de fallos individuales ---
        total_fallos_ping = 0
        for nombre, ip in PING_DESTINOS.items():
            ok, lat = ping(ETH2_IP, ip)
            resultados_ping[nombre] = ok
            lat_text = f"{lat} ms" if lat else "-"
            
            if not ok:
                total_fallos_ping += 1
            
            if ok:
                if estado_anterior[nombre] is False:
                    registrar_log(f"✅ RESTAURADO: {nombre} ({ip}) ha vuelto a estar accesible.")
                fallos_consecutivos[nombre] = 0
            else:
                if estado_anterior[nombre] is True or estado_anterior[nombre] is None:
                    registrar_log(f"❌ FALLO INICIADO: {nombre} ({ip}) no es accesible.")
                fallos_consecutivos[nombre] += 1

            estado_anterior[nombre] = ok
            print(f"[PING] {nombre} ({ip}): {'✅ OK' if ok else '❌ FALLO'} ({lat_text})")

        # --- Diagnóstico general y estado de fallo ---
        diagnostico = diagnosticar(resultados_ping)
        print(f"📡 Diagnóstico general: {diagnostico}")

        # Contar fallos consecutivos del diagnóstico general (solo si no es TODO OK)
        if total_fallos_ping > 0:
            # Incrementa si hay algún fallo en los switches
            fallos_consecutivos["GENERAL"] = fallos_consecutivos.get("GENERAL", 0) + 1
        else:
            fallos_consecutivos["GENERAL"] = 0

        # Determinar el estado de fallo general (is_failing)
        # Se considera fallando si hay al menos un fallo PING
        is_failing = total_fallos_ping > 0
        
        # --- Contador de Intermitencia (Drop Events) ---
        if not was_failing and is_failing:
            # Transición de OK a FALLO
            drop_events_count += 1
            registrar_log(f"🔔 Evento de caída de Switch detectado (OK -> FAIL). Contador de intermitencia: {drop_events_count}/{INTERMITTENCY_FAILURE_THRESHOLD}")

        # =======================================================
        # --- Lógica de NOTIFICACIÓN DE RESTABLECIMIENTO ---
        # =======================================================
        if was_failing and not is_failing:
            
            # Solo enviar restauración si se había enviado la alerta inicial
            if initial_alert_sent:
                motivo_restauracion = "RESTABLECIMIENTO DETECTADO"
                # Pasar resultados_http como un diccionario vacío, ya que la función lo espera
                mensaje_restauracion = generar_mensaje_alerta(timestamp, diagnostico, motivo_restauracion, resultados_ping, PING_DESTINOS)
                
                registrar_log("✅ Notificación de restablecimiento de Switches enviada. Reseteando variables de alerta.")
                
                enviar_telegram(mensaje_restauracion)
                enviar_email(f"✅ RESTABLECIMIENTO SENTINELA SWITCHES - {motivo_restauracion}", mensaje_restauracion)
            
            # Resetear variables de estado para el próximo fallo
            drop_events_count = 0
            initial_alert_sent = False
            indice_intervalo_telegram = 0
            # Establecer las últimas alertas a 'ahora' para evitar una alerta de fallo inmediata
            ultima_alerta["telegram"] = ahora 
            ultima_alerta["email"] = ahora 
        
        # =======================================================
        # --- Lógica de ALERTA INICIAL Y SECUENCIAL ---
        # =======================================================
        if is_failing:
            
            # Condición para la PRIMERA ALERTA (umbral de fallos alcanzado)
            is_persistent_failure = fallos_consecutivos["GENERAL"] >= CONSECUTIVE_FAILURE_THRESHOLD
            is_intermittent_failure = drop_events_count >= INTERMITTENCY_FAILURE_THRESHOLD
            
            if not initial_alert_sent:
                
                motivo_alerta = ""
                if is_persistent_failure:
                    motivo_alerta = f"FALLO PERSISTENTE (Detectado en {CONSECUTIVE_FAILURE_THRESHOLD} lecturas)"
                elif is_intermittent_failure:
                    motivo_alerta = f"ALERTA DE INESTABILIDAD (Detectadas {INTERMITTENCY_FAILURE_THRESHOLD} caídas recientes)."
                else:
                    # Esperando umbral (menos de 3 fallos consecutivos)
                    registrar_log(f"⌛ Fallo de Switch en curso, esperando umbral: Consecutivos={fallos_consecutivos['GENERAL']}, Intermitencia={drop_events_count}")
                    pass # No alertar todavía, solo esperar
                    
                
                if is_persistent_failure or is_intermittent_failure:
                    
                    # Generar y enviar la primera alerta inmediata
                    mensaje = generar_mensaje_alerta(timestamp, diagnostico, motivo_alerta, resultados_ping, PING_DESTINOS)
                    
                    registrar_log(f"🚨 ALERTA INICIAL SWITCHES ENVIADA por: {motivo_alerta}")
                    
                    enviar_telegram(mensaje)
                    enviar_email(f"⚠️ ALERTA SENTINELA SWITCHES - {motivo_alerta}", mensaje)
                    
                    # Marcar como enviado y resetear contadores para el manejo de intervalos
                    initial_alert_sent = True
                    drop_events_count = 0 # Reiniciar el contador de intermitencia ya que se alertó sobre ello
                    indice_intervalo_telegram = 0
                    ultima_alerta["telegram"] = ahora
                    ultima_alerta["email"] = ahora
            
            # Lógica para ALERTAS DE INTERVALO (solo si la inicial ya fue enviada)
            if initial_alert_sent:
                motivo_alerta_recurrente = "FALLO EN CURSO - ALERTA PROGRAMADA"
                mensaje = generar_mensaje_alerta(timestamp, diagnostico, motivo_alerta_recurrente, resultados_ping, PING_DESTINOS)

                # 1. Alerta Telegram (Tiempos secuenciales)
                current_interval_min = INTERVALOS_TELEGRAM_MIN[indice_intervalo_telegram]
                if (ahora - ultima_alerta["telegram"]) >= timedelta(minutes=current_interval_min):
                    try:
                        enviar_telegram(mensaje)
                        ultima_alerta["telegram"] = ahora
                        # Avanzar al siguiente intervalo de tiempo
                        if indice_intervalo_telegram < len(INTERVALOS_TELEGRAM_MIN) - 1:
                            indice_intervalo_telegram += 1

                    except Exception:
                        pass # El error ya fue registrado en enviar_telegram

                # 2. Alerta Email (Intervalo fijo de 6 horas)
                if (ahora - ultima_alerta["email"]) >= timedelta(hours=INTERVALO_EMAIL_H):
                    try:
                        enviar_email("⚠️ ALERTA SENTINELA SWITCHES - FALLO PERSISTENTE EN CURSO", mensaje)
                        ultima_alerta["email"] = ahora
                    except Exception:
                        pass # El error ya fue registrado en enviar_email
        
        # --- Actualizar estado para la próxima iteración ---
        was_failing = is_failing
        
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()
