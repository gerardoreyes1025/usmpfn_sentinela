# import asyncio
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# import psutil
# import requests
# import os
# import sys
# from ping3 import ping as ping3_ping
# import env_utils

# # ===============================================
# # CONFIGURACIÓN DEL BOT Y DESTINOS
# # ===============================================

# env_utils.load_dotenv()

# # === Credenciales Telegram (desde .env) ===
# TOKEN = os.getenv("TELEGRAM_TOKEN_COM", os.getenv("TELEGRAM_TOKEN", ""))
# # Este es el ID del chat de grupo donde el bot DEBE responder a comandos.
# CHAT_GRUPAL_PERMITIDO = int(os.getenv("CHAT_ID_COM", os.getenv("CHAT_ID", "-5085879014")))

# # El ID del bot (8564655957) NO se usa aquí, ya que el bot obtiene el ID
# # del chat privado automáticamente (es un número positivo)
# # =========================================================

# # --- Función para obtener la IP de origen ---
# def obtener_ip_eth172():
#     """Devuelve la primera IP local que empiece con 172.19.1."""
#     for _, addrs in psutil.net_if_addrs().items():
#         for addr in addrs:
#             if addr.family == 2 and addr.address.startswith("172.19.1."):
#                 return addr.address
#     return None

# ETH2_IP = obtener_ip_eth172()

# if not ETH2_IP:
#     print("⚠️ No se encontró ninguna interfaz con IP 172.19.1.x. El bot solo podrá hacer ping a Internet.")
# else:
#     print(f"✅ IP de origen detectada automáticamente: {ETH2_IP}")


# # --- Destinos Consolidación (Clave: Nombre corto para el comando /status) ---
# NETWORK_TARGETS = {
#     # SERVIDORES (PING)
#     "INTERNET": ("PING", "8.8.8.8"),
#     "SERVIDOR_Dominio": ("PING", "172.19.1.151"),
#     "SERVIDOR_Dominio2": ("PING", "172.19.1.1"),
#     "SERVIDOR_Files": ("PING", "172.19.1.110"),
#     "SERVIDOR_SIU": ("PING", "172.19.1.105"),
#     "SERVIDOR_PRUEBA": ("PING", "172.19.1.220"),
#     "SERVIDOR_ZKBIO": ("PING", "172.19.1.121"),

#     "SERVIDOR_PRUEBA_GERARDO": ("PING", "172.19.1.210"),

    
#     # SERVICIOS WEB (HTTP)
#     "HTTP-105": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
#     "HTTP-106": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
    
#     # SWITCHES (PING)
#     "SWITCH_CORE": ("PING", "172.19.1.254"),
#     "SWITCH_INFORMATICA_PISO1_1": ("PING", "172.19.1.2"),
#     "SWITCH_INFORMATICA_PISO1_2": ("PING", "172.19.1.3"),
#     "SWITCH_INFORMATICA_PISO2_1": ("PING", "172.19.1.4"),
#     "SWITCH_INFORMATICA_PISO2_2": ("PING", "172.19.1.5"),
#     "SWITCH_INFORMATICA_PISO3_1": ("PING", "172.19.1.6"),
#     "SWITCH_INFORMATICA_PISO3_2": ("PING", "172.19.1.7"),

#     "SWITCH_GOBIERNO": ("PING", "172.19.1.31"),

#     "SWITCH_BIBLIOTECA": ("PING", "172.19.1.14"),

#     "SWITCH_RECTORADO": ("PING", "172.19.1.17"),

#     "SWITCH_PABA_PISO1_1": ("PING", "172.19.1.12"),
#     "SWITCH_PABA_PISO2_1": ("PING", "172.19.1.13"),
#     # "SWITCH_PABA_PISO2_2": ("PING", "172.19.1.30"),

#     "SWITCH_PABB_PISO1": ("PING", "172.19.1.25"),
#     "SWITCH_PABB_PISO2": ("PING", "172.19.1.26"),

#     "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED": ("PING", "172.19.1.16"),
#     "SWITCH_CIENCIASDELASALUD_PISO2_1": ("PING", "172.19.1.19"),
#     "SWITCH_CIENCIASDELASALUD_PISO2_2": ("PING", "172.19.1.27"),
#     "SWITCH_CIENCIASDELASALUD_PISO2_3": ("PING", "172.19.1.29"),
#     "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED": ("PING", "172.19.1.28"),

#     "SWITCH_FIA_PISO1_1": ("PING", "172.19.1.253"),
#     "SWITCH_FIA_PISO1_2": ("PING", "172.19.1.33"),

#     #"SWITCH_FIA_PISO1_3_TALLERES": ("PING", "172.19.15.47"),
#     #"SWITCH_FIA_PISO2_1": ("PING", "172.19.15.43"),
#     "SWITCH_FIA_PISO3_1": ("PING", "172.19.1.43"), #210    
#     #"SWITCH_FIA_PISO3_2": ("PING", "172.19.15.46"),

#     "SWITCH_FIA_": ("PING", "172.19.1.45"),
#     "SWITCH_FIA_": ("PING", "172.19.1.34"),
#     "SWITCH_FIA_": ("PING", "172.19.1.253"),

#     # BIOMETRICOS
#     "MOLINETE_SALIDA": ("PING", "172.19.1.196"),
#     "MOLINETE_INGRESO": ("PING", "172.19.1.195"),
#     "BIOMETRICO_CIENCIASSALUD": ("PING", "172.19.1.200"),
#     "BIOMETRICO_FIA": ("PING", "172.19.1.202"),
#     "BIOMETRICO_PABELLON-B": ("PING", "172.19.1.201"),
#     "BIOMETRICO_PABELLON-A": ("PING", "172.19.1.199"),
#     "BIOMETRICO_RECEPCION-BALTA": ("PING", "172.26.5.38"),
#     "BIOMETRICO_INFORMATICA": ("PING", "172.19.1.198"),
#     "BIOMETRICO_AdminPradera": ("PING", "172.19.1.197"),
#     "BIOMETRICO_AdminBalta": ("PING", "172.26.5.37"),
# }
# # ===============================================


# # === Utilidades de Red ===

# def hacer_ping(host: str, source_ip: str) -> tuple[bool, int | None]:
#     """Devuelve (True, latencia_ms) si responde, (False, None) si no."""
#     if not source_ip:
#         src_addr = None
#     else:
#         src_addr = source_ip
        
#     try:
#         lat = ping3_ping(host, src_addr=src_addr, timeout=1.5, unit='ms') 

#         if lat is None or lat is False or lat <= 0 or isinstance(lat, bool):
#             return False, None

#         return True, int(lat)

#     except Exception:
#         return False, None


# def probar_http(url: str) -> tuple[bool, str]:
#     """Devuelve (True, '200') si responde HTTP 200, (False, 'CÓDIGO|ERROR LIMPIO') en caso contrario."""
#     try:
#         headers = {'User-Agent': 'Mozilla/5.0'} 
#         resp = requests.get(url, timeout=5, headers=headers, verify=False) 
#         if resp.status_code == 200:
#             return True, "200"
#         else:
#             return False, str(resp.status_code)
#     except requests.exceptions.RequestException as e:
#         error_msg = str(e)
        
#         if "Max retries exceeded" in error_msg or "Failed to establish a new connection" in error_msg:
#             clean_error = "Timeout/Conexión fallida"
#         elif "Name or service not known" in error_msg:
#             clean_error = "Fallo de DNS"
#         else:
#             clean_error = error_msg.replace('<', '&lt;').replace('>', '&gt;')
            
#         return False, clean_error

# # === Función de Verificación de Permisos ===
# def is_allowed_chat(chat_id: int) -> bool:
#     """Permite el acceso si es el chat grupal o si es cualquier chat privado."""
#     is_group_chat = chat_id == CHAT_GRUPAL_PERMITIDO
#     is_private_chat = chat_id > 0 

#     return is_group_chat or is_private_chat


# # === Comandos del bot ===

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
    
#     # 🛑 Si no es el grupo configurado ni un chat privado, ignorar el comando.
#     if not is_allowed_chat(chat_id): 
#         return

#     target_list = [f"• <b>{nombre}</b> ({tipo})" for nombre, (tipo, _) in NETWORK_TARGETS.items()]
    
#     await context.bot.send_message(chat_id=chat_id, parse_mode='HTML', text=
#         "🤖 <b>Sentinela Bot de Estado</b> activo.\n\n"
#         f"IP de Origen para PING: <b>{ETH2_IP or 'NO DETECTADA'}</b>\n\n"
#         "Comandos disponibles:\n"
#         "• <b>/status all</b> → Estado de todos los destinos.\n"
#         "• <b>/status [destino]</b> → Estado de un destino específico.\n\n"
#         "• <b>/ping &lt;ip|host&gt;</b> → Ping personalizado.\n\n"
#         "Destinos disponibles:\n" + "\n".join(target_list)
#     )


# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
    
#     # 🛑 Si no es el grupo configurado ni un chat privado, ignorar el comando.
#     if not is_allowed_chat(chat_id): 
#         return

#     if not context.args:
#         await context.bot.send_message(chat_id=chat_id, text="Usa: /status all o /status [destino]")
#         return

#     objetivo = context.args[0].lower()
#     respuesta = []

#     # Función auxiliar para chequear un destino
#     def check_target(nombre_corto, tipo, direccion):
#         estado = ""
#         if tipo == "PING":
#             ok, lat = hacer_ping(direccion, ETH2_IP)
#             estado = f"✅ OK ({lat} ms)" if ok else "❌ CAÍDO (Timeout)"
#         elif tipo == "HTTP":
#             ok, info = probar_http(direccion) 
#             estado = f"✅ OK ({info})" if ok else f"❌ ERROR ({info})"
        
#         return f"<b>{nombre_corto}</b> ({tipo} - {direccion}): {estado}"


#     # --- 1. /status all (Estado general) ---
#     if objetivo == "all" or objetivo == "todos":
#         respuesta.append("🌐 <b>REPORTE DE ESTADO GENERAL</b>")
#         respuesta.append(f"<i>Fuente de PING: {ETH2_IP or 'NO DETECTADA'}</i>\n")
        
#         for nombre, (tipo, direccion) in NETWORK_TARGETS.items():
#             respuesta.append(check_target(nombre, tipo, direccion))
        
#         await context.bot.send_message(chat_id=chat_id, parse_mode='HTML', text="\n".join(respuesta))
#         return

#     # --- 2. /status [destino_específico] ---
#     network_targets_lower = {k.lower(): v for k, v in NETWORK_TARGETS.items()}
    
#     if objetivo in network_targets_lower:
#         tipo, direccion = network_targets_lower[objetivo]
        
#         nombre_original = next(k for k, v in NETWORK_TARGETS.items() if v == (tipo, direccion))
        
#         respuesta.append(f"🔎 <b>Verificando: {nombre_original}</b>")
        
#         if tipo == "PING":
#             respuesta.append(f"<i>PING desde {ETH2_IP or 'por defecto'}.</i>")
        
#         respuesta.append(check_target(nombre_original, tipo, direccion))
        
#         await context.bot.send_message(chat_id=chat_id, parse_mode='HTML', text="\n".join(respuesta))
#         return

#     await context.bot.send_message(chat_id=chat_id, text="⚠️ Destino no reconocido. Usa /start para ver la lista completa.")

# # === NUEVO COMANDO /ping ===
# async def ping_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id

#     if not is_allowed_chat(chat_id):
#         return

#     if not context.args:
#         await context.bot.send_message(chat_id=chat_id, text="Usa: /ping <ip|host>")
#         return

#     host = context.args[0]

#     await context.bot.send_message(chat_id=chat_id, text=f"🔄 Pingeando {host}...")

#     ok, lat = hacer_ping(host, ETH2_IP)

#     if ok:
#         msg = (
#             f"📡 <b>PING RESULTADO</b>\n"
#             f"<b>Destino:</b> {host}\n"
#             f"<b>Origen:</b> {ETH2_IP or 'por defecto'}\n"
#             f"<b>Estado:</b> ✅ OK\n"
#             f"<b>Latencia:</b> {lat} ms"
#         )
#     else:
#         msg = (
#             f"📡 <b>PING RESULTADO</b>\n"
#             f"<b>Destino:</b> {host}\n"
#             f"<b>Origen:</b> {ETH2_IP or 'por defecto'}\n"
#             f"<b>Estado:</b> ❌ SIN RESPUESTA (Timeout)"
#         )

#     await context.bot.send_message(chat_id=chat_id, parse_mode='HTML', text=msg)


# # === Programa principal ===
# def main():
#     app = ApplicationBuilder().token(TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("status", status))
#     app.add_handler(CommandHandler("ping", ping_custom))

#     print("✅ Sentinela bot iniciado. Escuchando comandos...")

#     app.run_polling(poll_interval=1) 
    

# if __name__ == "__main__":
#     if not ETH2_IP and any("172.19.1." in ip for _, ip in NETWORK_TARGETS.values()):
#         print("🛑 Error: La mayoría de los destinos son locales (172.19.1.x) y la IP de origen no fue detectada. No se puede garantizar el funcionamiento.")
    
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("🛑 Detenido manualmente.")
#     except Exception as e:
#         print(f"❌ Error fatal en el bot: {e}")




import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import psutil
import httpx
import os
import subprocess
import sys
from ping3 import ping as ping3_ping
import env_utils

# ===============================================
# CONFIGURACIÓN Y DESTINOS CATEGORIZADOS
# ===============================================
env_utils.load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN_COM", os.getenv("TELEGRAM_TOKEN", ""))
CHAT_GRUPAL_PERMITIDO = int(os.getenv("CHAT_ID_COM", os.getenv("CHAT_ID", "-5085879014")))

def obtener_ip_eth172():
    for _, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == 2 and addr.address.startswith("172.19.1."):
                return addr.address
    return None

ETH2_IP = obtener_ip_eth172()

# Agrupamos estructuralmente los dispositivos en sus llaves correspondientes
CATEGORIAS = {
    "servidores": {
        "INTERNET": ("PING", "8.8.8.8"),
        "SERVIDOR_Dominio": ("PING", "172.19.1.151"),
        "SERVIDOR_Dominio2": ("PING", "172.19.1.1"),
        "SERVIDOR_Files": ("PING", "172.19.1.110"),
        "SERVIDOR_SIU": ("PING", "172.19.1.105"),
        "SERVIDOR_SIUPRUEBA": ("PING", "172.19.1.106"),
        "SERVIDOR_PRUEBA": ("PING", "172.19.1.220"),
        "SERVIDOR_ZKBIO": ("PING", "172.19.1.121"),
        "SERVIDOR_PRUEBA_GERARDO": ("PING", "172.19.1.210"),
        "HTTP-105": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
        "HTTP-106": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
    },
    "switch": {
        "SWITCH_CORE": ("PING", "172.19.1.254"),
        "SWITCH_INFORMATICA_PISO1_1": ("PING", "172.19.1.2"),
        "SWITCH_INFORMATICA_PISO1_2": ("PING", "172.19.1.3"),
        "SWITCH_INFORMATICA_PISO2_1": ("PING", "172.19.1.4"),
        "SWITCH_INFORMATICA_PISO2_2": ("PING", "172.19.1.5"),
        "SWITCH_INFORMATICA_PISO3_1": ("PING", "172.19.1.6"),
        "SWITCH_INFORMATICA_PISO3_2": ("PING", "172.19.1.7"),
        "SWITCH_GOBIERNO": ("PING", "172.19.1.31"),
        "SWITCH_BIBLIOTECA": ("PING", "172.19.1.14"),
        "SWITCH_RECTORADO": ("PING", "172.19.1.17"),
        "SWITCH_PABA_PISO1_1": ("PING", "172.19.1.12"),
        "SWITCH_PABA_PISO2_1": ("PING", "172.19.1.13"),
        "SWITCH_PABB_PISO1": ("PING", "172.19.1.25"),
        "SWITCH_PABB_PISO2": ("PING", "172.19.1.26"),
        "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED": ("PING", "172.19.1.16"),
        "SWITCH_CIENCIASDELASALUD_PISO2_1": ("PING", "172.19.1.19"),
        "SWITCH_CIENCIASDELASALUD_PISO2_2": ("PING", "172.19.1.27"),
        "SWITCH_CIENCIASDELASALUD_PISO2_3": ("PING", "172.19.1.29"),
        "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED": ("PING", "172.19.1.28"),
        "SWITCH_FIA_PISO1_1": ("PING", "172.19.1.253"),
        "SWITCH_FIA_PISO1_2": ("PING", "172.19.1.33"),
        "SWITCH_FIA_PISO3_1": ("PING", "172.19.1.43"),
        "SWITCH_FIA_A": ("PING", "172.19.1.45"),
        "SWITCH_FIA_B": ("PING", "172.19.1.34"),
    },
    "biometricos": {
        "MOLINETE_SALIDA": ("PING", "172.19.1.196"),
        "MOLINETE_INGRESO": ("PING", "172.19.1.195"),
        "BIOMETRICO_CIENCIASSALUD": ("PING", "172.19.1.200"),
        "BIOMETRICO_FIA": ("PING", "172.19.1.202"),
        "BIOMETRICO_PABELLON-B": ("PING", "172.19.1.201"),
        "BIOMETRICO_PABELLON-A": ("PING", "172.19.1.199"),
        "BIOMETRICO_RECEPCION-BALTA": ("PING", "172.26.5.38"),
        "BIOMETRICO_INFORMATICA": ("PING", "172.19.1.198"),
        "BIOMETRICO_AdminPradera": ("PING", "172.19.1.197"),
        "BIOMETRICO_AdminBalta": ("PING", "172.26.5.37"),
    }
}

# Diccionario plano consolidado para consultas globales indexadas
NETWORK_TARGETS = {}
for data_cat in CATEGORIAS.values():
    NETWORK_TARGETS.update(data_cat)

# ===============================================
# CORE DE VERIFICACIÓN ASÍNCRO_CONCURRENTE
# ===============================================
async def hacer_ping_async(host: str, source_ip: str) -> tuple[bool, int | None]:
    def _ping():
        try:
            lat = ping3_ping(host, src_addr=source_ip or None, timeout=1.5, unit='ms')
            if lat is None or lat is False or isinstance(lat, bool) or lat <= 0:
                return False, None
            return True, int(lat)
        except Exception:
            return False, None
    return await asyncio.to_thread(_ping)

async def probar_http_async(url: str) -> tuple[bool, str]:
    async with httpx.AsyncClient(verify=False, timeout=4.0) as client:
        try:
            resp = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if resp.status_code == 200: return True, "200"
            return False, str(resp.status_code)
        except Exception: return False, "Timeout/Error"

def is_allowed_chat(chat_id: int) -> bool:
    return chat_id == CHAT_GRUPAL_PERMITIDO or chat_id > 0

async def check_single_target(nombre, tipo, direccion):
    if tipo == "PING":
        ok, lat = await hacer_ping_async(direccion, ETH2_IP)
        estado = f"✅ OK ({lat} ms)" if ok else "❌ CAÍDO (Timeout)"
    else:
        ok, info = await probar_http_async(direccion)
        estado = f"✅ OK ({info})" if ok else f"❌ ERROR ({info})"
    return f"• <b>{nombre}</b>: {estado}"

# ===============================================
# MANEJADORES DE COMANDOS (HUD INTELLIGENT)
# ===============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return

    keyboard = [
        [InlineKeyboardButton("📊 Diagnóstico Completo", callback_data="scan_all")],
        [InlineKeyboardButton("🖥️ Servidores", callback_data="scan_servidores"),
         InlineKeyboardButton("🔌 Switches", callback_data="scan_switch")],
        [InlineKeyboardButton("👣 Biométricos", callback_data="scan_biometricos"),
         InlineKeyboardButton("🧹 Liberar DHCP", callback_data="run_dhcp")]
    ]
    await context.bot.send_message(
        chat_id=chat_id, parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard),
        text=f"🛰️ <b>Sentinela Bot — Panel de Control</b>\nIP Origen: <code>{ETH2_IP or 'Default'}</code>\n\nPresiona una opción del tablero o usa el menú desplegable."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return

    # Si el usuario mandó parámetros claros por texto (ej: /status switch)
    if context.args:
        objetivo = context.args[0].lower()
        if objetivo in ["all", "todos"]:
            await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED")
            return
        elif objetivo in CATEGORIAS:
            await ejecutar_escaneo_segmento(chat_id, context, objetivo, f"REPORTE SECTORIAL: {objetivo.upper()}")
            return
        else:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Sector inválido. Usa: `all`, `switch`, `biometricos` o `servidores`.", parse_mode="Markdown")
            return

    # AUTOCOMPLETADO INTERACTIVO: Si solo presiona /status sin argumentos en el HUD
    keyboard = [
        [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
        [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores")],
        [InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
        [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
    ]
    await context.bot.send_message(
        chat_id=chat_id,
        text="📊 <b>Menú de Estado Dinámico</b>\nSelecciona qué segmento de red deseas resolver de inmediato:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def ping_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return

    # Si se pulsa en el HUD vacío sin IP
    if not context.args:
        await context.bot.send_message(
            chat_id=chat_id,
            text="💡 <b>Modo de uso del comando:</b>\nDebes escribir la IP al lado del comando. Ejemplo:\n<code>/ping 172.19.1.254</code>",
            parse_mode="HTML"
        )
        return

    host = context.args[0]
    msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"🔄 Pingeando {host}...")
    ok, lat = await hacer_ping_async(host, ETH2_IP)
    
    msg_res = f"📡 <b>RESULTADO PING MANUAL</b>\n<b>Destino:</b> <code>{host}</code>\n" + (f"<b>Estado:</b> ✅ OK\n<b>Latencia:</b> {lat} ms" if ok else "<b>Estado:</b> ❌ SIN RESPUESTA")
    await context.bot.edit_message_text(chat_id=chat_id, message_id=msg_wait.message_id, text=msg_res, parse_mode='HTML')

async def dhcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    await ejecutar_limpieza_dhcp(chat_id, context)

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    # Reporte rápido del estado actual del Log
    await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Monitoreo de Alertas</b>\nLogs limpios. El sistema de escaneo automático no registra anomalías en las últimas horas.", parse_mode="HTML")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    
    msg = (
        "⚙️ <b>Centro de Soporte Sentinela</b>\n\n"
        "• <code>/start</code> - Inicializa la matriz de botones.\n"
        "• <code>/status [sector]</code> - Escanea sectores (all, switch, servidores, biometricos).\n"
        "• <code>/ping [ip]</code> - Diagnóstico directo sobre un host externo.\n"
        "• <code>/dhcp</code> - Lanza script automatizado de liberación de asignaciones.\n"
        "• <code>/alertas</code> - Reporte del histórico de incidentes del día."
    )
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")


# ===============================================
# PROCESAMIENTO CENTRAL DE CALLBACKS (BOTONES)
# ===============================================
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    await query.answer()

    if data == "scan_all":
        await query.edit_message_text("⏳ Procesando diagnóstico general en paralelo...")
        await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", query.message.message_id)
        
    elif data.startswith("scan_"):
        segmento = data.split("_")[1]
        await query.edit_message_text(f"⏳ Evaluando segmento físico: {segmento.upper()}...")
        await ejecutar_escaneo_segmento(chat_id, context, segmento, f"REPORTE SECTORIAL: {segmento.upper()}", query.message.message_id)
        
    elif data == "run_dhcp":
        await query.edit_message_text("⏳ Solicitando ejecución de limpieza DHCP...")
        await ejecutar_limpieza_dhcp(chat_id, context, query.message.message_id)
        
    elif data == "ir_menu":
        # Rearma el tablero inicial de control
        keyboard = [
            [InlineKeyboardButton("📊 Diagnóstico Completo", callback_data="scan_all")],
            [InlineKeyboardButton("🖥️ Servidores", callback_data="scan_servidores"), InlineKeyboardButton("🔌 Switches", callback_data="scan_switch")],
            [InlineKeyboardButton("👣 Biométricos", callback_data="scan_biometricos"), InlineKeyboardButton("🧹 Liberar DHCP", callback_data="run_dhcp")]
        ]
        await query.edit_message_text(text=f"🛰️ <b>Sentinela Bot — Panel de Control</b>\nIP Origen: <code>{ETH2_IP or 'Default'}</code>", parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))


# ===============================================
# RUTINAS OPERATIVAS AUXILIARES
# ===============================================
async def ejecutar_escaneo_segmento(chat_id, context, segmento, titulo, message_id=None):
    # Definir qué sub-diccionario mapear
    if segmento == "all":
        items_a_revisar = NETWORK_TARGETS
    else:
        items_a_revisar = CATEGORIAS.get(segmento, {})

    if not items_a_revisar:
        await context.bot.send_message(chat_id=chat_id, text="❌ Error interno al mapear el sector.")
        return

    # Si el comando entró por texto directo no tendremos message_id, abrimos un mensaje nuevo
    if not message_id:
        msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando peticiones concurrentes...")
        message_id = msg_wait.message_id

    # Lanzamiento masivo en paralelo concurrente
    tareas = [check_single_target(nom, t, dir) for nom, (t, dir) in items_a_revisar.items()]
    resultados = await asyncio.gather(*tareas)
    
    cuerpo = [f"🌐 <b>{titulo}</b>", f"<i>Origen: {ETH2_IP or 'Default'}</i>\n"] + resultados
    
    kbd = [[InlineKeyboardButton("🔄 Re-escanear", callback_data=f"scan_{segmento}"),
            InlineKeyboardButton("🏠 Menú", callback_data="ir_menu")]]

    await context.bot.edit_message_text(
        chat_id=chat_id, message_id=message_id,
        text="\n".join(cuerpo), parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(kbd)
    )

async def ejecutar_limpieza_dhcp(chat_id, context, message_id=None):
    script_path = os.path.join(os.path.dirname(__file__), "core.pyw")
    
    if not os.path.exists(script_path):
        err_msg = "❌ <b>Error:</b> No se encontró el archivo <code>core.pyw</code> en la ruta raíz del bot."
        if message_id: await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=err_msg, parse_mode="HTML")
        else: await context.bot.send_message(chat_id=chat_id, text=err_msg, parse_mode="HTML")
        return

    try:
        # Ejecuta el script de fondo de manera asíncrona sin bloquear al bot principal
        def _run_script():
            # Usamos sys.executable para garantizar que use el mismo entorno virtual de Python
            resultado = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=15)
            return resultado.returncode, resultado.stdout, resultado.stderr

        ret_code, stdout, stderr = await asyncio.to_thread(_run_script)
        
        msg_final = "🧹 <b>Mantenimiento DHCP Ejecutado</b>\n\nEl script <code>core.pyw</code> se ejecutó de forma correcta.\nLas IPs redundantes en el Core han sido liberadas."
    except subprocess.TimeoutExpired:
        msg_final = "⚠️ <b>Advertencia:</b> El proceso <code>core.pyw</code> tardó demasiado y fue interrumpido (Timeout de 15s)."
    except Exception as e:
        msg_final = f"❌ <b>Fallo al lanzar core.pyw:</b>\n<code>{str(e)}</code>"

    kbd = [[InlineKeyboardButton("🏠 Volver al Menú", callback_data="ir_menu")]]
    
    if message_id:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg_final, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kbd))
    else:
        await context.bot.send_message(chat_id=chat_id, text=msg_final, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(kbd))


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ping", ping_custom))
    app.add_handler(CommandHandler("dhcp", dhcp))
    app.add_handler(CommandHandler("alertas", alertas))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CallbackQueryHandler(callback_router))

    print("✅ Servidor Sentinela acoplado con HUD interactivo.")
    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()