from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import psutil
import os
from ping3 import ping as ping3_ping

# ==============================
# CONFIGURACIÓN GENERAL DEL SENTINELA
# ==============================

# --- CREDENCIALES Y URL ---
URL_BASE = "https://172.19.1.121:8098/main.do?home&selectSysCode=Acc"
USUARIO = "admin"
PASSWORD_VISIBLE = "fILIALNORTEUSMP400" 

# --- CONFIGURACIÓN DE LOG ---
LOG_FILE = r"C:\SentryLogs\sentinela_log_biometricos.txt" 

# --- INVENTARIO FIJO ESPERADO (Nombre: IP) ---
FIXED_DEVICES_INVENTORY = {
    "SALIDA": ("PING", "172.19.1.196"),
    "INGRESO": ("PING", "172.19.1.195"),
    "CIENCIASSALUD": ("PING", "172.19.1.200"),
    "FIA": ("PING", "172.19.1.202"),
    "PABELLON-B": ("PING", "172.19.1.201"),
    "PABELLON-A": ("PING", "172.19.1.199"),
    "RECEPCION-BALTA": ("PING", "172.26.5.38"),
    "INFORMATICA": ("PING", "172.19.1.198"),
}

# --- NUEVOS DISPOSITIVOS SOLO PING ---
PING_ONLY_DEVICES = {
    "BIOMETRICO-AdminPradera": "172.19.1.197",
    "BIOMETRICO-AdminBalta": "172.26.5.37",
}

FIXED_DEVICE_NAMES = list(FIXED_DEVICES_INVENTORY.keys())
PING_ONLY_NAMES = list(PING_ONLY_DEVICES.keys())
ALL_DEVICE_NAMES = FIXED_DEVICE_NAMES + PING_ONLY_NAMES

# --- CONFIGURACIÓN DE ALERTAS Y TIEMPOS ---
# SCAN_INTERVAL_SECONDS se usa para RECOVERY Mode.
SCAN_INTERVAL_SECONDS = 60 
SLEEP_INTERVAL_SECONDS = 3 * 60 * 60 # 4 horas (14400 segundos)
FAILURE_CONFIRMATIONS_REQUIRED = 10 
RECOVERY_CONFIRMATIONS_REQUIRED = 10 # <--- ACTUALIZADO a 5 (Estabilidad al restablecer)

# --- NUEVAS CONFIGURACIONES PARA EL MODO BURST ---
BURST_CYCLES = 15             # Número de ciclos de escaneo rápido al despertar
BURST_INTERVAL_SECONDS = 60   # Intervalo entre ciclos en modo BURST

# --- CONFIGURACIÓN TELEGRAM Y EMAIL (¡ACTUALIZAR!) ---
# ¡REEMPLAZAR ESTOS VALORES POR LOS CREDENCIALES DEL CANAL DE SWITCHES!
TELEGRAM_TOKEN = "8509545584:AAH7wgNuxvGdkERhokjTqGunKXBYpxFqnJw"#"8443835269:AAGb8b3IjMhncS1fkEsUTatHpTkU3yE8tAA"#"8564655957:AAEoH57-SCEe0TIISiXZFoOeayaCjkSFCcQ" 
CHAT_ID = -5095804558
# ---------------------------------------------

# Email (usando tus credenciales proporcionadas)
EMAIL_FROM = "gramosr@usmp.pe"
EMAIL_TO = ["gramosr@usmp.pe", "scalleg@usmp.pe", "ecasasv@usmp.pe", "icajusola@usmp.pe", "rsoberonb@usmp.pe","lfernandezc@usmp.pe", "vmanayayc@usmp.pe"]
EMAIL_PASS = "Kingstonk62*"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

# ==============================
# FUNCIONES DE UTILIDAD (Log, Email, Telegram, Ping)
# ==============================

def registrar_log(mensaje):
    """Guarda en el log solo errores o eventos relevantes."""
    try:
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {mensaje}\n")
    except Exception as e:
        print(f"❌ Error al escribir en el log {LOG_FILE}: {e}")
        
def escape_html(text):
    if not isinstance(text, str):
        text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def enviar_telegram(mensaje, motivo):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}, timeout=10)
        if response.status_code == 200 and response.json().get('ok'):
            registrar_log(f"📲 Notificación de Telegram ({motivo}) enviada exitosamente.")
        else:
            error_msg = response.json().get('description', 'Error desconocido en la respuesta de Telegram.')
            registrar_log(f"❌ Error al enviar Telegram ({motivo}) (Status {response.status_code}): {error_msg}")
    except Exception as e:
        registrar_log(f"❌ Error Telegram ({motivo}): {e}")

def enviar_email(asunto, mensaje, motivo):
    msg = MIMEText(mensaje, "html")
    msg["Subject"] = asunto
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        registrar_log(f"📧 Correo electrónico ({motivo}) enviado exitosamente.")
    except Exception as e:
        registrar_log(f"❌ Error correo ({motivo}): {e}")

def ping(destino):
    """Devuelve (True, latencia_ms) si responde; (False, None) si no."""
    ip_origen = None 
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2 and addr.address.startswith("172.19."):
                ip_origen = addr.address
                break
        if ip_origen:
            break
            
    try:
        lat = ping3_ping(destino, src_addr=ip_origen, timeout=1, unit='ms') 
        if lat is None or lat is False or lat <= 0 or isinstance(lat, bool):
            return False, None
        return True, int(lat)
    except Exception as e:
        return False, None

# ==============================
# FUNCIONES DE EXTRACCIÓN (SELENIUM)
# ==============================

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        registrar_log(f"❌ Error al iniciar el WebDriver: {e}.")
        return None

def get_registration_state(cell):
    """Determina si el dispositivo está registrado (check/x) buscando el ícono."""
    try:
        cell.find_element(By.CSS_SELECTOR, "div.icon_state_yes")
        return "Registrado (Sí)"
    except:
        return "No Registrado (No)"

def login_and_extract_devices(driver):
    """Realiza el login, navega, y extrae la lista de dispositivos."""
    wait = WebDriverWait(driver, 60) 
    device_list = []
    
    try:
        # 1. Acceder y Login
        driver.get(URL_BASE)
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(USUARIO)
        driver.find_element(By.ID, "password").send_keys(PASSWORD_VISIBLE)
        
        try:
            xpath_checkbox = "//div[@class='login-protocol']//input[@name='serviceProtocol']"
            checkbox = wait.until(EC.presence_of_element_located((By.XPATH, xpath_checkbox)))
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
        except Exception:
             pass
            
        driver.find_element(By.ID, "test").click()
        
        # 2. Navegación
        wait.until(EC.presence_of_element_located((By.ID, "AccMenu")))
        time.sleep(3) 
        ACC_MENU_XPATH = "//a[@id='AccMenu']"
        acc_menu_element = wait.until(EC.presence_of_element_located((By.XPATH, ACC_MENU_XPATH)))
        driver.execute_script("arguments[0].click();", acc_menu_element)
        time.sleep(5) 

        # 3. Limpiar overlays
        driver.execute_script("document.querySelectorAll('.dhx_modal_cover, .guide-box').forEach(el => el.remove());")
        time.sleep(1)
        
        # 4. Extracción de datos
        table_body_xpath = "//div[@class='dhxgrid_box']//div[@class='objbox']//table//tbody"
        wait.until(EC.presence_of_element_located((By.XPATH, table_body_xpath)))
        wait.until(EC.presence_of_element_located((By.XPATH, f"{table_body_xpath}/tr[2]"))) 
        rows = driver.find_elements(By.XPATH, f"{table_body_xpath}/tr")
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 10: 
                device_info = {
                    "Dispositivo": cells[1].text.strip(), 
                    "IP": cells[6].text.strip(),         
                    "Estado": cells[8].text.strip(),     
                    "Registro": get_registration_state(cells[10]) 
                }
                device_list.append(device_info)
        
        registrar_log(f"✅ Extracción completada. {len(device_list)} dispositivos encontrados.")
        return device_list

    except Exception as e:
        registrar_log(f"❌ ERROR DE EXTRACCIÓN (Selenium/Login falló): {type(e).__name__} - {e}")
        return []

# ==============================
# LÓGICA DE ALERTA Y MONITOREO
# ==============================

def generar_alerta_biometricos(timestamp, motivo, fallos_activos, inventory_for_report):
    """Genera el cuerpo del mensaje de alerta."""
    
    emoji_principal = "🚨" if "FALLO" in motivo or "DESAPARECIDO" in motivo else "✅"
    
    mensaje = f"<b>{emoji_principal} ALERTA SENTINELA BIOMÉTRICOS {emoji_principal}</b>\n"
    mensaje += f"Hora: {timestamp}\n"
    mensaje += f"Motivo: <b>{motivo}</b>\n\n"
    
    fallos_reportados = [d for d in fallos_activos if d.get('Reported', False)]

    if fallos_reportados:
        mensaje += "<b>🔴 Dispositivos con Fallo Reportado:</b>\n"
        for f in fallos_reportados:
            ip = f.get('IP', FIXED_DEVICES_INVENTORY.get(f['Dispositivo'], PING_ONLY_DEVICES.get(f['Dispositivo'], 'N/A')))
            mensaje += f"❌ <b>{escape_html(f['Dispositivo'])}</b> (IP: {ip})\n"
            
            # Solo mostrar estado Web/Registro si no es solo Ping
            if f['Dispositivo'] in FIXED_DEVICE_NAMES:
                estado_web = f.get('Estado', 'N/A')
                if estado_web == 'DESAPARECIDO':
                     estado_web = 'No Encontrado en Web'
                     
                mensaje += f"   - Estado Web: {escape_html(estado_web)} | Registro: {f.get('Registro', 'N/A')}\n"
            
            ping_status = "✅ OK" if f.get('Ping_OK') else "❌ FALLÓ"
            ping_lat = f"({f['Ping_Lat']} ms)" if f.get('Ping_Lat') else ""
            mensaje += f"   - Diagnóstico Ping: {ping_status} {ping_lat}\n"
        mensaje += "\n"
        
    # Discrepancia de inventario (solo para los que deberían estar en la web)
    encontrados_web = {d['Dispositivo'] for d in inventory_for_report if d['Dispositivo'] in FIXED_DEVICE_NAMES and d.get('Estado') != 'DESAPARECIDO'}
    
    if len(encontrados_web) != len(FIXED_DEVICES_INVENTORY):
        mensaje += f"<b>⚠️ Discrepancia de Inventario Web:</b>\n"
        nombres_fijos = set(FIXED_DEVICE_NAMES)
        desaparecidos = nombres_fijos - encontrados_web
        
        if desaparecidos:
            mensaje += f"   - <b>Desaparecidos de la Web</b>: {', '.join(desaparecidos)}\n"
        
        mensaje += "\n"
        
    mensaje += "<b>🟢 Estado Actual (Web/Ping):</b>\n"
    
    for name in ALL_DEVICE_NAMES:
        d = device_states.get(name, {})
        if not d: continue 
        
        # Criterio de OK
        is_ok = d.get('Ping_OK')
        if name in FIXED_DEVICE_NAMES:
            is_ok = is_ok and d.get('Estado') == "Conectado" and d.get('Registro') == "Registrado (Sí)"
        
        ip = d.get('IP', FIXED_DEVICES_INVENTORY.get(name, PING_ONLY_DEVICES.get(name, 'N/A')))
        estado_emoji = "✅" if is_ok else "❌"

        # Descripción del estado
        if name in FIXED_DEVICE_NAMES:
            if d.get('Estado') == 'DESAPARECIDO':
                estado_desc = '❌ DESAPARECIDO (No en web)'
            else:
                estado_desc = f"[Web: {d.get('Estado', 'N/A')} | Reg: {d.get('Registro', 'N/A')}]"
        else: # Solo Ping
            estado_desc = "[Solo Ping]"

        ping_res = "Ping OK" if d.get('Ping_OK') else "Ping FALLA"
        
        mensaje += f"{estado_emoji} {escape_html(name)} ({ip}) {estado_desc} | {ping_res}\n"

    return mensaje

device_states = {}

def update_device_states(extracted_devices):
    """Actualiza el estado, contador de fallos y ping de los dispositivos, incluyendo solo-ping."""
    
    global device_states
    
    extracted_names = {d['Dispositivo'] for d in extracted_devices}
    new_device_states = {}
    
    # Inicialización para todos los dispositivos (fijos y solo ping)
    if not device_states:
        for name, ip in {**FIXED_DEVICES_INVENTORY, **PING_ONLY_DEVICES}.items():
            device_states[name] = {'IP': ip, 'FailCount': 0, 'Reported': False, 'RecoveryCount': 0, 'Estado': 'N/A', 'Registro': 'N/A', 'Ping_OK': False, 'Ping_Lat': None}


    # --- 1. Procesar dispositivos extraídos (Inventario Fijo) ---
    for device in extracted_devices:
        name = device['Dispositivo']
        ip = device['IP']
        
        state = device_states.get(name, {'IP': ip, 'FailCount': 0, 'Reported': False, 'RecoveryCount': 0})
        state['IP'] = ip
        state['Estado'] = device['Estado']
        state['Registro'] = device['Registro']
        
        ping_ok, ping_lat = ping(ip)
        state['Ping_OK'] = ping_ok
        state['Ping_Lat'] = ping_lat

        # Criterio de Fallo Fijo: Desconectado O No Registrado O Ping Falla
        is_failing_now = (state['Estado'] != "Conectado") or \
                         (state['Registro'] != "Registrado (Sí)") or \
                         (not ping_ok)
        
        if is_failing_now:
            if not state['Reported']:
                state['FailCount'] += 1
                state['RecoveryCount'] = 0
            else:
                state['RecoveryCount'] = 0
                state['FailCount'] = min(state['FailCount'] + 1, FAILURE_CONFIRMATIONS_REQUIRED + 1)
                
        else:
            if state['Reported']:
                state['RecoveryCount'] += 1
                state['FailCount'] = 0
            else:
                state['FailCount'] = 0
                state['RecoveryCount'] = 0
                
        new_device_states[name] = state

    # --- 2. Manejo de dispositivos desaparecidos (Inventario Fijo) ---
    for name in FIXED_DEVICE_NAMES:
        if name not in extracted_names:
            ip_fija = FIXED_DEVICES_INVENTORY[name]
            
            state = device_states.get(name, {'IP': ip_fija, 'FailCount': 0, 'Reported': False, 'RecoveryCount': 0})
            
            state['Estado'] = 'DESAPARECIDO'
            state['Registro'] = 'No Registrado (No)'
            state['IP'] = ip_fija 
            
            ping_ok, ping_lat = ping(ip_fija)
            state['Ping_OK'] = ping_ok
            state['Ping_Lat'] = ping_lat
            
            # Siempre es fallo si desapareció
            is_failing_now = True 
            
            if not state['Reported']:
                state['FailCount'] += 1
                state['RecoveryCount'] = 0
            else:
                state['RecoveryCount'] = 0
                state['FailCount'] = min(state['FailCount'] + 1, FAILURE_CONFIRMATIONS_REQUIRED + 1)

            new_device_states[name] = state

    # --- 3. Procesar dispositivos Solo Ping (Ping Only Devices) ---
    for name in PING_ONLY_NAMES:
        ip = PING_ONLY_DEVICES[name]
        
        state = device_states.get(name, {'IP': ip, 'FailCount': 0, 'Reported': False, 'RecoveryCount': 0, 'Estado': 'Solo Ping', 'Registro': 'N/A'})
        
        ping_ok, ping_lat = ping(ip)
        state['Ping_OK'] = ping_ok
        state['Ping_Lat'] = ping_lat
        state['IP'] = ip
        
        # Criterio de Fallo Solo Ping: Ping Falla
        is_failing_now = (not ping_ok)

        if is_failing_now:
            if not state['Reported']:
                state['FailCount'] += 1
                state['RecoveryCount'] = 0
            else:
                state['RecoveryCount'] = 0
                state['FailCount'] = min(state['FailCount'] + 1, FAILURE_CONFIRMATIONS_REQUIRED + 1)
        else:
            if state['Reported']:
                state['RecoveryCount'] += 1
                state['FailCount'] = 0
            else:
                state['FailCount'] = 0
                state['RecoveryCount'] = 0
        
        new_device_states[name] = state

    device_states = new_device_states
    
    # Generar la lista completa (fijos + solo ping) para el reporte de alerta
    inventory_for_report = [] 
    for name in ALL_DEVICE_NAMES:
        state = device_states.get(name)
        if state:
            report_entry = state.copy()
            report_entry['Dispositivo'] = name
            inventory_for_report.append(report_entry)
            
    return inventory_for_report


def monitor_biometrics():
    """Bucle principal de monitoreo de Biométricos con modos SLEEP, BURST_SCAN y RECOVERY."""
    
    global device_states
    
    # in_sleep empieza en True para forzar el primer BURST_SCAN
    in_sleep = False
    burst_cycle_count = 0 
    last_telegram_alert_time = datetime.min
    last_email_alert_time = datetime.min
    
    print(f"--- Sentinela de Biométricos iniciado ({datetime.now().strftime('%H:%M')}) ---")
    registrar_log("--- Sentinela de Biométricos iniciado. ---")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ahora = datetime.now()
        
        is_failing_reported = any(s.get('Reported', False) for s in device_states.values())
        
        # --- Lógica de Transición de Modos ---
        if is_failing_reported:
            current_mode = "RECOVERY"
            in_sleep = False
            burst_cycle_count = 0
            
        elif in_sleep:
            current_mode = "SLEEP"
            
        elif burst_cycle_count < BURST_CYCLES:
            current_mode = "BURST_SCAN"
            
        else: # Burst completado sin fallos reportados
            current_mode = "SLEEP" # Transicionar a SLEEP en el siguiente ciclo
            
        print(f"\n--- 🔄 Iniciando ciclo. Modo actual: {current_mode} --- ({timestamp})")
        
        # 1. Modo SLEEP (4 horas)
        if current_mode == "SLEEP":
            print(f"😴 Modo SLEEP. Esperando {int(SLEEP_INTERVAL_SECONDS/60)} minutos para el próximo escaneo.")
            time.sleep(SLEEP_INTERVAL_SECONDS)
            in_sleep = False # Al despertar, salimos de sleep para iniciar BURST_SCAN
            burst_cycle_count = 0 
            continue
            
        # --- MODOS DE ESCANEO (RECOVERY / BURST_SCAN) ---
        
        # 2. Setup Driver, Extracción y Quit Driver
        extracted_devices = []
        driver = setup_driver()
        if not driver: 
            registrar_log("❌ No se pudo iniciar el driver. Reintentando en el próximo ciclo.")
            time.sleep(SCAN_INTERVAL_SECONDS)
            continue
        
        try:
            print("1. Ejecutando extracción de datos de la web (Nueva sesión)...")
            extracted_devices = login_and_extract_devices(driver)
        finally:
            driver.quit()
        
        # --- DEBUGGING: Mostrar la data cruda extraída ---
        print("\n*** 🚨 DATA CRUDA EXTRAÍDA DE LA WEB: ***")
        if extracted_devices:
            for d in extracted_devices:
                print(f"    -> {d}")
        else:
            print("    -> Lista de dispositivos vacía (Error en Selenium o web vacía).")
        print("*********************************************\n")
        # ----------------------------------------------------
        
        # 3. Analizar datos, realizar Ping y actualizar estados de Fallo/Recuperación
        inventory_for_report = update_device_states(extracted_devices)

        # 4. Mostrar estado del Ping en Consola
        print("2. Verificación de Ping y Fallo (Inventario Fijo + Solo Ping):")
        
        # --- CREACIÓN DE LISTAS DE ALERTA ---
        devices_to_report = []
        devices_to_restore = []
        active_failing_devices = []
        
        for name in ALL_DEVICE_NAMES:
            d = device_states.get(name, {})
            if not d: continue
            
            # Copiamos el estado y añadimos el nombre del dispositivo para la función de alerta
            device_data = d.copy()
            device_data['Dispositivo'] = name 

            ip = d.get('IP', FIXED_DEVICES_INVENTORY.get(name, PING_ONLY_DEVICES.get(name, 'N/A')))
            ping_ok = d.get('Ping_OK')
            fail_count = d.get('FailCount', 0)
            
            # Consola: Estado de Fallo
            is_fixed_device = name in FIXED_DEVICES_INVENTORY
            
            if is_fixed_device:
                ping_target = f"(IP Web: {ip})" if d.get('Estado') != 'DESAPARECIDO' else f"(IP Fija: {ip})"
                is_ok = ping_ok and d.get('Estado') == "Conectado" and d.get('Registro') == "Registrado (Sí)"
                ok_status_msg = f"OK (Web/Reg OK, {d.get('Ping_Lat')} ms)"
            else:
                ping_target = f"(IP Solo Ping: {ip})"
                is_ok = ping_ok
                ok_status_msg = f"OK (Ping OK, {d.get('Ping_Lat')} ms)"
                
            if is_ok:
                print(f"   ✅ {name:<20}: {ping_target} -> {ok_status_msg}")
            else:
                emoji = "❌" if fail_count < FAILURE_CONFIRMATIONS_REQUIRED else "🔥"
                fail_status = f"Fallos: {fail_count}"
                if d.get('Reported'): fail_status = f"🚨 REPORTADO (Rec: {d.get('RecoveryCount')}/{RECOVERY_CONFIRMATIONS_REQUIRED}) 🚨"
                print(f"   {emoji} {name:<20}: {ping_target} -> FALLANDO ({fail_status})")
                
            # Lógica de Reporte
            if d['FailCount'] >= FAILURE_CONFIRMATIONS_REQUIRED and not d['Reported']:
                devices_to_report.append(device_data)
                
            if d['RecoveryCount'] >= RECOVERY_CONFIRMATIONS_REQUIRED and d['Reported']:
                devices_to_restore.append(device_data)

            if d['Reported'] or d['FailCount'] > 0:
                active_failing_devices.append(device_data)
        # --------------------------------------------------

        # 5. Determinar acciones de alerta
        
        inventory_discrepancy = (len([d for d in extracted_devices if d['Dispositivo'] in FIXED_DEVICE_NAMES]) != len(FIXED_DEVICES_INVENTORY))
        
        # --- A. ALERTAS DE FALLO (Reporte Inicial) ---
        if devices_to_report or (inventory_discrepancy and (ahora - last_telegram_alert_time) >= timedelta(seconds=SCAN_INTERVAL_SECONDS*2)):
            
            for d in devices_to_report:
                # Si se reporta un fallo, salimos inmediatamente del BURST y entramos a RECOVERY
                in_sleep = False
                burst_cycle_count = 0
                
                device_states[d['Dispositivo']]['Reported'] = True
                registrar_log(f"🚨 ALERTA INICIAL - {d['Dispositivo']} alcanzó {FAILURE_CONFIRMATIONS_REQUIRED} fallos consecutivos.")

            if devices_to_report:
                motivo = f"FALLO PERSISTENTE DETECTADO ({len(devices_to_report)} Dispositivo(s))"
            else:
                motivo = "FALLO DE INVENTARIO (Dispositivos Faltantes/Sobrantes en Web)"


            mensaje = generar_alerta_biometricos(timestamp, motivo, active_failing_devices, inventory_for_report)
            enviar_telegram(mensaje, "FALLO_INICIAL")
            enviar_email(f"🚨 ALERTA BIOMÉTRICOS - {motivo}", mensaje, "FALLO_INICIAL")
            last_telegram_alert_time = ahora
            last_email_alert_time = ahora
            
        # --- B. ALERTAS DE RESTABLECIMIENTO ---
        if devices_to_restore:
            motivo = "✅ RESTABLECIMIENTO TOTAL DETECTADO"
            
            for d in devices_to_restore:
                # Actualizamos el estado de REPORTED en el device_states global
                device_states[d['Dispositivo']]['Reported'] = False
                device_states[d['Dispositivo']]['FailCount'] = 0
                device_states[d['Dispositivo']]['RecoveryCount'] = 0
                registrar_log(f"✅ RESTAURADO - {d['Dispositivo']} volvió a estar OK ({RECOVERY_CONFIRMATIONS_REQUIRED} confirmaciones).")

            mensaje = generar_alerta_biometricos(timestamp, motivo, [], inventory_for_report) 
            enviar_telegram(mensaje, "RESTABLECIDO")
            enviar_email(f"✅ RESTABLECIMIENTO BIOMÉTRICOS", mensaje, "RESTABLECIDO")
            last_telegram_alert_time = ahora
            last_email_alert_time = ahora
        
        # 6. Esperar el intervalo apropiado y gestionar el estado BURST
        
        if current_mode == "RECOVERY":
            print(f"\n3. Modo RECOVERY. Esperando {SCAN_INTERVAL_SECONDS} segundos para el próximo ciclo.")
            time.sleep(SCAN_INTERVAL_SECONDS)
            
        elif current_mode == "BURST_SCAN":
            burst_cycle_count += 1
            print(f"\n3. Modo BURST SCAN ({burst_cycle_count}/{BURST_CYCLES}). Esperando {BURST_INTERVAL_SECONDS} segundos para el próximo ciclo.")
            time.sleep(BURST_INTERVAL_SECONDS)
            
            # Si el burst termina, el próximo ciclo de while hará la transición a SLEEP
            if burst_cycle_count == BURST_CYCLES:
                 in_sleep = True 


# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    try:
        monitor_biometrics()
    except KeyboardInterrupt:
        print("\nScript detenido por el usuario.")
    except Exception as e:
        registrar_log(f"❌ ERROR CRÍTICO EN EL BUCLE PRINCIPAL: {e}")
        print(f"❌ ERROR CRÍTICO EN EL BUCLE PRINCIPAL: {e}")
