# # import asyncio
# # from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# # from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
# # import psutil
# # import httpx
# # import os
# # import subprocess
# # import sys
# # from ping3 import ping as ping3_ping
# # import env_utils

# # # ===============================================
# # # CONFIGURACIÓN Y DESTINOS CATEGORIZADOS
# # # ===============================================
# # env_utils.load_dotenv()
# # TOKEN = os.getenv("TELEGRAM_TOKEN_COM", os.getenv("TELEGRAM_TOKEN", ""))
# # CHAT_GRUPAL_PERMITIDO = int(os.getenv("CHAT_ID_COM", os.getenv("CHAT_ID", "-5085879014")))

# # def obtener_ip_eth172():
# #     for _, addrs in psutil.net_if_addrs().items():
# #         for addr in addrs:
# #             if addr.family == 2 and addr.address.startswith("172.19.1."):
# #                 return addr.address
# #     return None

# # ETH2_IP = obtener_ip_eth172()

# # CATEGORIAS = {
# #     "servidores": {
# #         "INTERNET": ("PING", "8.8.8.8"),
# #         "SERVIDOR_Dominio": ("PING", "172.19.1.151"),
# #         "SERVIDOR_Dominio2": ("PING", "172.19.1.1"),
# #         "SERVIDOR_Files": ("PING", "172.19.1.110"),
# #         "SERVIDOR_SIU": ("PING", "172.19.1.105"),
# #         "SERVIDOR_PRUEBA": ("PING", "172.19.1.220"),
# #         "SERVIDOR_ZKBIO": ("PING", "172.19.1.121"),
# #         "SERVIDOR_PRUEBA_GERARDO": ("PING", "172.19.1.210"),
# #         "HTTP-105": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
# #         "HTTP-106": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
# #     },
# #     "switch": {
# #         "SWITCH_CORE": ("PING", "172.19.1.254"),
# #         "SWITCH_INFORMATICA_PISO1_1": ("PING", "172.19.1.2"),
# #         "SWITCH_INFORMATICA_PISO1_2": ("PING", "172.19.1.3"),
# #         "SWITCH_INFORMATICA_PISO2_1": ("PING", "172.19.1.4"),
# #         "SWITCH_INFORMATICA_PISO2_2": ("PING", "172.19.1.5"),
# #         "SWITCH_INFORMATICA_PISO3_1": ("PING", "172.19.1.6"),
# #         "SWITCH_INFORMATICA_PISO3_2": ("PING", "172.19.1.7"),
# #         "SWITCH_GOBIERNO": ("PING", "172.19.1.31"),
# #         "SWITCH_BIBLIOTECA": ("PING", "172.19.1.14"),
# #         "SWITCH_RECTORADO": ("PING", "172.19.1.17"),
# #         "SWITCH_PABA_PISO1_1": ("PING", "172.19.1.12"),
# #         "SWITCH_PABA_PISO2_1": ("PING", "172.19.1.13"),
# #         "SWITCH_PABB_PISO1": ("PING", "172.19.1.25"),
# #         "SWITCH_PABB_PISO2": ("PING", "172.19.1.26"),
# #         "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED": ("PING", "172.19.1.16"),
# #         "SWITCH_CIENCIASDELASALUD_PISO2_1": ("PING", "172.19.1.19"),
# #         "SWITCH_CIENCIASDELASALUD_PISO2_2": ("PING", "172.19.1.27"),
# #         "SWITCH_CIENCIASDELASALUD_PISO2_3": ("PING", "172.19.1.29"),
# #         "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED": ("PING", "172.19.1.28"),
# #         "SWITCH_FIA_PISO1_1": ("PING", "172.19.1.253"),
# #         "SWITCH_FIA_PISO1_2": ("PING", "172.19.1.33"),
# #         "SWITCH_FIA_PISO3_1": ("PING", "172.19.1.43"),
# #         "SWITCH_FIA_A": ("PING", "172.19.1.45"),
# #         "SWITCH_FIA_B": ("PING", "172.19.1.34"),
# #     },
# #     "biometricos": {
# #         "MOLINETE_SALIDA": ("PING", "172.19.1.196"),
# #         "MOLINETE_INGRESO": ("PING", "172.19.1.195"),
# #         "BIOMETRICO_CIENCIASSALUD": ("PING", "172.19.1.200"),
# #         "BIOMETRICO_FIA": ("PING", "172.19.1.202"),
# #         "BIOMETRICO_PABELLON-B": ("PING", "172.19.1.201"),
# #         "BIOMETRICO_PABELLON-A": ("PING", "172.19.1.199"),
# #         "BIOMETRICO_RECEPCION-BALTA": ("PING", "172.26.5.38"),
# #         "BIOMETRICO_INFORMATICA": ("PING", "172.19.1.198"),
# #         "BIOMETRICO_AdminPradera": ("PING", "172.19.1.197"),
# #         "BIOMETRICO_AdminBalta": ("PING", "172.26.5.37"),
# #     }
# # }

# # NETWORK_TARGETS = {}
# # for data_cat in CATEGORIAS.values():
# #     NETWORK_TARGETS.update(data_cat)

# # # ===============================================
# # # CORE DE VERIFICACIÓN ASÍNCRONA
# # # ===============================================
# # async def hacer_ping_async(host: str, source_ip: str) -> tuple[bool, int | None]:
# #     def _ping():
# #         try:
# #             lat = ping3_ping(host, src_addr=source_ip or None, timeout=1.5, unit='ms')
# #             if lat is None or lat is False or isinstance(lat, bool) or lat <= 0:
# #                 return False, None
# #             return True, int(lat)
# #         except Exception:
# #             return False, None
# #     return await asyncio.to_thread(_ping)

# # async def probar_http_async(url: str) -> tuple[bool, str]:
# #     async with httpx.AsyncClient(verify=False, timeout=4.0) as client:
# #         try:
# #             resp = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# #             if resp.status_code == 200: return True, "200"
# #             return False, str(resp.status_code)
# #         except Exception: return False, "Timeout/Error"


# # CHAT_GRUPAL_PERMITIDO = int(os.getenv("CHAT_ID_COM", "-5085879014"))
# # raw_users = os.getenv("USERS_PERMITIDOS", "")
# # USUARIOS_AUTORIZADOS = [int(uid.strip()) for uid in raw_users.split(",") if uid.strip()]

# # # Fusionamos todo en un conjunto global de IDs permitidos (Grupo + Staff de TI)
# # IDS_PERMITIDOS = [CHAT_GRUPAL_PERMITIDO] + USUARIOS_AUTORIZADOS

# # def is_allowed_chat(chat_id: int) -> bool:
# #     """Retorna True únicamente si el chat_id figura en la lista explícita del .env"""
# #     return chat_id in IDS_PERMITIDOS

# # # def is_allowed_chat(chat_id: int) -> bool:
# # #     return chat_id == CHAT_GRUPAL_PERMITIDO or chat_id > 0


# # async def check_single_target(nombre, tipo, direccion):
# #     if tipo == "PING":
# #         ok, lat = await hacer_ping_async(direccion, ETH2_IP)
# #         estado = f"• <b>{nombre}</b>: ✅ OK ({lat} ms)" if ok else f"• <b>{nombre}</b>: ❌ CAÍDO"
# #     else:
# #         ok, info = await probar_http_async(direccion)
# #         estado = f"• <b>{nombre}</b>: ✅ OK ({info})" if ok else f"• <b>{nombre}</b>: ❌ ERROR ({info})"
# #     return estado


# # # ===============================================
# # # FUNCIÓN REUTILIZABLE PARA EL PANEL (NUNCA BORRA)
# # # ===============================================
# # async def enviar_panel_principal(context, chat_id):
# #     keyboard = [
# #         [InlineKeyboardButton("📊 Diagnóstico Completo", callback_data="scan_all")],
# #         [InlineKeyboardButton("📁 Ver por Categorías", callback_data="menu_status")],
# #         [InlineKeyboardButton("📡 Lanzar Ping Manual", callback_data="solicitar_ping"),
# #          InlineKeyboardButton("🧹 Liberar DHCP", callback_data="run_dhcp")]
# #     ]
# #     await context.bot.send_message(
# #         chat_id=chat_id, parse_mode='HTML',
# #         reply_markup=InlineKeyboardMarkup(keyboard),
# #         text=f"🛰️ <b>Sentinela Bot — Panel de Control</b>\nIP Origen: <code>{ETH2_IP or 'Default'}</code>\n\nPresiona una opción del tablero o usa el menú nativo."
# #     )


# # # ===============================================
# # # MANEJADORES DE COMANDOS (HUD)
# # # ===============================================

# # async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return
# #     context.user_data["esperando_ip"] = False
# #     await enviar_panel_principal(context, chat_id)

# # async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return
# #     context.user_data["esperando_ip"] = False

# #     if context.args:
# #         objetivo = context.args[0].lower()
# #         if objetivo in ["all", "todos"]:
# #             await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED")
# #             return
# #         elif objetivo in CATEGORIAS:
# #             await ejecutar_escaneo_segmento(chat_id, context, objetivo, f"REPORTE SECTORIAL: {objetivo.upper()}")
# #             return
# #         else:
# #             await context.bot.send_message(chat_id=chat_id, text="⚠️ Sector inválido. Usa: `all`, `switch`, `biometricos` o `servidores`.", parse_mode="Markdown")
# #             return

# #     keyboard = [
# #         [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
# #         [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"),
# #          InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
# #         [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
# #     ]
# #     await context.bot.send_message(
# #         chat_id=chat_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard),
# #         text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona qué segmento de red deseas resolver:"
# #     )

# # async def ping_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return

# #     if context.args:
# #         context.user_data["esperando_ip"] = False
# #         host = context.args[0]
# #         await procesar_y_responder_ping(chat_id, host, context)
# #         return

# #     context.user_data["esperando_ip"] = True
# #     await context.bot.send_message(
# #         chat_id=chat_id, parse_mode="HTML",
# #         text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe a continuación la IP o Host que deseas verificar."
# #     )

# # async def texto_libre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return

# #     if context.user_data.get("esperando_ip"):
# #         context.user_data["esperando_ip"] = False
# #         host = update.message.text.strip()
# #         await procesar_y_responder_ping(chat_id, host, context)
# #     else:
# #         await context.bot.send_message(chat_id=chat_id, text="⚠️ Comando no reconocido. Utiliza el botón <b>Menú</b> o ejecuta /start para abrir el panel.", parse_mode="HTML")

# # async def procesar_y_responder_ping(chat_id, host, context):
# #     msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"🔄 Ejecutando ICMP hacia {host}...")
# #     ok, lat = await hacer_ping_async(host, ETH2_IP)
    
# #     msg_res = f"📡 <b>RESULTADO PING MANUAL</b>\n<b>Destino:</b> <code>{host}</code>\n" + (f"<b>Estado:</b> ✅ OK\n<b>Latencia:</b> {lat} ms" if ok else "<b>Estado:</b> ❌ SIN RESPUESTA")
    
# #     await context.bot.edit_message_text(chat_id=chat_id, message_id=msg_wait.message_id, text=msg_res, parse_mode='HTML')
# #     # Invocamos el menú de nuevo de forma independiente para mantener el flujo abajo
# #     await enviar_panel_principal(context, chat_id)

# # async def dhcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return
# #     context.user_data["esperando_ip"] = False
# #     await ejecutar_limpieza_dhcp(chat_id, context)

# # async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return
# #     context.user_data["esperando_ip"] = False
# #     await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Monitoreo de Alertas</b>\nLogs limpios. Sin novedades en el segmento.", parse_mode="HTML")

# # async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     chat_id = update.effective_chat.id
# #     if not is_allowed_chat(chat_id): return
# #     context.user_data["esperando_ip"] = False
    
# #     msg = (
# #         "⚙️ <b>Centro de Soporte Sentinela</b>\n\n"
# #         "• <code>/start</code> - Inicializa la matriz de botones.\n"
# #         "• <code>/status [sector]</code> - Escanea sectores.\n"
# #         "• <code>/ping</code> - Pide IP en el siguiente input.\n"
# #         "• <code>/dhcp</code> - Ejecuta liberación core.pyw."
# #     )
# #     await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")


# # # ===============================================
# # # PROCESADOR DE BOTONES (CALLBACKS)
# # # ===============================================
# # # async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
# # #     query = update.callback_query
# # #     data = query.data
# # #     chat_id = query.message.chat_id
# # #     await query.answer()
# # async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     query = update.callback_query
# #     chat_id = query.message.chat_id
    
# #     # SEGURIDAD: Si el chat no está autorizado, frena la acción de inmediato
# #     if not is_allowed_chat(chat_id):
# #         await query.answer("🚫 No tienes permisos de TI para usar este bot.", show_alert=True)
# #         return
        
# #     data = query.data
# #     await query.answer()
    
# #     if data == "scan_all":
# #         context.user_data["esperando_ip"] = False
# #         # Para mantener el historial intacto, notificamos en un mensaje nuevo en vez de editar el panel principal
# #         msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando diagnóstico general en paralelo...")
# #         await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", msg_wait.message_id)
        
# #     elif data.startswith("scan_"):
# #         context.user_data["esperando_ip"] = False
# #         segmento = data.split("_")[1]
# #         msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"⏳ Evaluando segmento físico: {segmento.upper()}...")
# #         await ejecutar_escaneo_segmento(chat_id, context, segmento, f"REPORTE SECTORIAL: {segmento.upper()}", msg_wait.message_id)
        
# #     elif data == "menu_status":
# #         context.user_data["esperando_ip"] = False
# #         keyboard = [
# #             [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
# #             [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"), InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
# #             [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
# #         ]
# #         # Cambiamos a mensaje nuevo para no pisar el start principal
# #         await context.bot.send_message(chat_id=chat_id, text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona el segmento de red:", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

# #     elif data == "solicitar_ping":
# #         context.user_data["esperando_ip"] = True
# #         # CORREGIDO: parse_mode='HTML' añadido para que aplique las negritas desde el botón
# #         await context.bot.send_message(chat_id=chat_id, text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe la IP o el Host a testear directamente en el teclado:", parse_mode='HTML')

# #     elif data == "run_dhcp":
# #         context.user_data["esperando_ip"] = False
# #         msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Solicitando ejecución de limpieza DHCP...")
# #         await ejecutar_limpieza_dhcp(chat_id, context, msg_wait.message_id)


# # # ===============================================
# # # RUTINAS OPERATIVAS AUXILIARES
# # # ===============================================
# # async def ejecutar_escaneo_segmento(chat_id, context, segmento, titulo, message_id):
# #     if segmento == "all": items_a_revisar = NETWORK_TARGETS
# #     else: items_a_revisar = CATEGORIAS.get(segmento, {})

# #     if not items_a_revisar: return

# #     tareas = [check_single_target(nom, t, dir) for nom, (t, dir) in items_a_revisar.items()]
# #     resultados = await asyncio.gather(*tareas)
    
# #     cuerpo = [f"🌐 <b>{titulo}</b>", f"<i>Origen: {ETH2_IP or 'Default'}</i>\n"] + resultados

# #     # Editamos el mensaje de carga ("Procesando...") con el reporte final
# #     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\n".join(cuerpo), parse_mode='HTML')
    
# #     # Volvemos a lanzar el panel principal limpio abajo en la cola para continuar operando sin perder la vista de arriba
# #     await enviar_panel_principal(context, chat_id)

# # async def ejecutar_limpieza_dhcp(chat_id, context, message_id):
# #     script_path = os.path.join(os.path.dirname(__file__), "core.pyw")
# #     if not os.path.exists(script_path):
# #         await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ <b>Error:</b> No se encontró <code>core.pyw</code>.", parse_mode="HTML")
# #         return

# #     try:
# #         def _run_script():
# #             res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=15)
# #             return res.returncode
# #         await asyncio.to_thread(_run_script)
# #         msg_final = "🧹 <b>Mantenimiento DHCP Ejecutado</b>\nLas IPs redundantes en el Core han sido liberadas con éxito."
# #     except Exception as e:
# #         msg_final = f"❌ <b>Fallo al lanzar core.pyw:</b>\n<code>{str(e)}</code>"

# #     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg_final, parse_mode="HTML")
# #     await enviar_panel_principal(context, chat_id)


# # def main():
# #     app = ApplicationBuilder().token(TOKEN).build()

# #     app.add_handler(CommandHandler("start", start))
# #     app.add_handler(CommandHandler("status", status))
# #     app.add_handler(CommandHandler("ping", ping_custom))
# #     app.add_handler(CommandHandler("dhcp", dhcp))
# #     app.add_handler(CommandHandler("alertas", alertas))
# #     app.add_handler(CommandHandler("ayuda", ayuda))
# #     app.add_handler(CallbackQueryHandler(callback_router))
# #     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_libre_handler))

# #     print("✅ Servidor Sentinela acoplado con HUD interactivo.")
# #     app.run_polling(poll_interval=1)

# # if __name__ == "__main__":
# #     main()




# import asyncio
# import os
# import subprocess
# import sys
# import time
# from datetime import datetime
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import (
#     ApplicationBuilder,
#     CallbackQueryHandler,
#     CommandHandler,
#     ContextTypes,
#     MessageHandler,
#     filters,
# )
# import psutil
# import httpx
# from ping3 import ping as ping3_ping
# import env_utils

# # ===============================================
# # CONFIGURACIÓN Y DESTINOS CATEGORIZADOS
# # ===============================================
# env_utils.load_dotenv()
# TOKEN = os.getenv("TELEGRAM_TOKEN_COM", os.getenv("TELEGRAM_TOKEN", ""))
# CHAT_GRUPAL_PERMITIDO = int(os.getenv("CHAT_ID_COM", os.getenv("CHAT_ID", "-5085879014")))

# def obtener_ip_eth172():
#     for _, addrs in psutil.net_if_addrs().items():
#         for addr in addrs:
#             if addr.family == 2 and addr.address.startswith("172.19.1."):
#                 return addr.address
#     return None

# ETH2_IP = obtener_ip_eth172()

# CATEGORIAS = {
#     "servidores": {
#         "INTERNET": ("PING", "8.8.8.8"),
#         "SERVIDOR_Dominio": ("PING", "172.19.1.151"),
#         "SERVIDOR_Dominio2": ("PING", "172.19.1.1"),
#         "SERVIDOR_Files": ("PING", "172.19.1.110"),
#         "SERVIDOR_SIU": ("PING", "172.19.1.105"),
#         "SERVIDOR_PRUEBA": ("PING", "172.19.1.220"),
#         "SERVIDOR_ZKBIO": ("PING", "172.19.1.121"),
#         "SERVIDOR_PRUEBA_GERARDO": ("PING", "172.19.1.210"),
#         "HTTP-105": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
#         "HTTP-106": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
#     },
#     "switch": {
#         "SWITCH_CORE": ("PING", "172.19.1.254"),
#         "SWITCH_INFORMATICA_PISO1_1": ("PING", "172.19.1.2"),
#         "SWITCH_INFORMATICA_PISO1_2": ("PING", "172.19.1.3"),
#         "SWITCH_INFORMATICA_PISO2_1": ("PING", "172.19.1.4"),
#         "SWITCH_INFORMATICA_PISO2_2": ("PING", "172.19.1.5"),
#         "SWITCH_INFORMATICA_PISO3_1": ("PING", "172.19.1.6"),
#         "SWITCH_INFORMATICA_PISO3_2": ("PING", "172.19.1.7"),
#         "SWITCH_GOBIERNO": ("PING", "172.19.1.31"),
#         "SWITCH_BIBLIOTECA": ("PING", "172.19.1.14"),
#         "SWITCH_RECTORADO": ("PING", "172.19.1.17"),
#         "SWITCH_PABA_PISO1_1": ("PING", "172.19.1.12"),
#         "SWITCH_PABA_PISO2_1": ("PING", "172.19.1.13"),
#         "SWITCH_PABB_PISO1": ("PING", "172.19.1.25"),
#         "SWITCH_PABB_PISO2": ("PING", "172.19.1.26"),
#         "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED": ("PING", "172.19.1.16"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_1": ("PING", "172.19.1.19"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_2": ("PING", "172.19.1.27"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_3": ("PING", "172.19.1.29"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED": ("PING", "172.19.1.28"),
#         "SWITCH_FIA_PISO1_1": ("PING", "172.19.1.253"),
#         "SWITCH_FIA_PISO1_2": ("PING", "172.19.1.33"),
#         "SWITCH_FIA_PISO3_1": ("PING", "172.19.1.43"),
#         "SWITCH_FIA_A": ("PING", "172.19.1.45"),
#         "SWITCH_FIA_B": ("PING", "172.19.1.34"),
#     },
#     "biometricos": {
#         "MOLINETE_SALIDA": ("PING", "172.19.1.196"),
#         "MOLINETE_INGRESO": ("PING", "172.19.1.195"),
#         "BIOMETRICO_CIENCIASSALUD": ("PING", "172.19.1.200"),
#         "BIOMETRICO_FIA": ("PING", "172.19.1.202"),
#         "BIOMETRICO_PABELLON-B": ("PING", "172.19.1.201"),
#         "BIOMETRICO_PABELLON-A": ("PING", "172.19.1.199"),
#         "BIOMETRICO_RECEPCION-BALTA": ("PING", "172.26.5.38"),
#         "BIOMETRICO_INFORMATICA": ("PING", "172.19.1.198"),
#         "BIOMETRICO_AdminPradera": ("PING", "172.19.1.197"),
#         "BIOMETRICO_AdminBalta": ("PING", "172.26.5.37"),
#     }
# }

# NETWORK_TARGETS = {}
# for data_cat in CATEGORIAS.values():
#     NETWORK_TARGETS.update(data_cat)

# # ===============================================
# # FILTRO DE SEGURIDAD Y COOLDOWNS
# # ===============================================
# raw_users = os.getenv("USERS_PERMITIDOS", "")
# USUARIOS_AUTORIZADOS = [int(uid.strip()) for uid in raw_users.split(",") if uid.strip()]
# IDS_PERMITIDOS = [CHAT_GRUPAL_PERMITIDO] + USUARIOS_AUTORIZADOS

# def is_allowed_chat(chat_id: int) -> bool:
#     """Retorna True únicamente si el chat_id figura en la lista explícita del .env"""
#     return chat_id in IDS_PERMITIDOS

# COOLDOWNS = {}

# def verificar_cooldown(id_clave: int, tipo_accion: str, segundos_espera: int) -> tuple[bool, int]:
#     """Controla la saturación de ejecuciones repetidas por chat/grupo."""
#     ahora = time.time()
#     if id_clave not in COOLDOWNS:
#         COOLDOWNS[id_clave] = {}
#     ultima_vez = COOLDOWNS[id_clave].get(tipo_accion, 0)
#     tiempo_transcurrido = ahora - ultima_vez
#     if tiempo_transcurrido < segundos_espera:
#         return False, int(segundos_espera - tiempo_transcurrido)
#     COOLDOWNS[id_clave][tipo_accion] = ahora
#     return True, 0

# # ===============================================
# # CORE DE VERIFICACIÓN ASÍNCRONA
# # ===============================================
# async def hacer_ping_async(host: str, source_ip: str) -> tuple[bool, int | None]:
#     def _ping():
#         try:
#             lat = ping3_ping(host, src_addr=source_ip or None, timeout=1.5, unit='ms')
#             if lat is None or lat is False or isinstance(lat, bool) or lat <= 0:
#                 return False, None
#             return True, int(lat)
#         except Exception:
#             return False, None
#     return await asyncio.to_thread(_ping)

# async def probar_http_async(url: str) -> tuple[bool, str]:
#     async with httpx.AsyncClient(verify=False, timeout=4.0) as client:
#         try:
#             resp = await client.get(url, headers={'User-Agent': 'Mozilla/5.0'})
#             if resp.status_code == 200: return True, "200"
#             return False, str(resp.status_code)
#         except Exception: return False, "Timeout/Error"

# async def check_single_target(nombre, tipo, direccion):
#     if tipo == "PING":
#         ok, lat = await hacer_ping_async(direccion, ETH2_IP)
#         estado = f"• <b>{nombre}</b>: ✅ OK ({lat} ms)" if ok else f"• <b>{nombre}</b>: ❌ CAÍDO"
#     else:
#         ok, info = await probar_http_async(direccion)
#         estado = f"• <b>{nombre}</b>: ✅ OK ({info})" if ok else f"• <b>{nombre}</b>: ❌ ERROR ({info})"
#     return estado

# # ===============================================
# # FUNCIÓN REUTILIZABLE PARA EL PANEL
# # ===============================================
# async def enviar_panel_principal(context, chat_id):
#     keyboard = [
#         [InlineKeyboardButton("📊 Diagnóstico Completo", callback_data="scan_all")],
#         [InlineKeyboardButton("📁 Ver por Categorías", callback_data="menu_status")],
#         [InlineKeyboardButton("📡 Lanzar Ping Manual", callback_data="solicitar_ping"),
#          InlineKeyboardButton("🧹 Liberar DHCP", callback_data="run_dhcp")]
#     ]
#     await context.bot.send_message(
#         chat_id=chat_id, parse_mode='HTML',
#         reply_markup=InlineKeyboardMarkup(keyboard),
#         text=f"🛰️ <b>Sentinela Bot — Panel de Control</b>\nIP Origen: <code>{ETH2_IP or 'Default'}</code>\n\nPresiona una opción del tablero o usa el menú nativo."
#     )

# # ===============================================
# # MANEJADORES DE COMANDOS (HUD)
# # ===============================================
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return
#     context.user_data["esperando_ip"] = False
#     await enviar_panel_principal(context, chat_id)

# async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return
#     context.user_data["esperando_ip"] = False

#     if context.args:
#         objetivo = context.args[0].lower()
#         if objetivo in ["all", "todos"]:
#             puede, s = verificar_cooldown(chat_id, "scan_all", 30)
#             if not puede:
#                 await update.message.reply_text(f"⏳ Espera {s}s para un nuevo diagnóstico masivo.")
#                 return
#             msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando diagnóstico general...")
#             await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", msg_wait.message_id)
#             return
#         elif objetivo in CATEGORIAS:
#             msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"⏳ Evaluando {objetivo.upper()}...")
#             await ejecutar_escaneo_segmento(chat_id, context, objetivo, f"REPORTE SECTORIAL: {objetivo.upper()}", msg_wait.message_id)
#             return
#         else:
#             await context.bot.send_message(chat_id=chat_id, text="⚠️ Sector inválido. Usa: `all`, `switch`, `biometricos` o `servidores`.", parse_mode="Markdown")
#             return

#     keyboard = [
#         [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
#         [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"), InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
#         [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
#     ]
#     await context.bot.send_message(
#         chat_id=chat_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard),
#         text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona qué segmento de red deseas resolver:"
#     )

# async def ping_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return

#     if context.args:
#         context.user_data["esperando_ip"] = False
#         await procesar_y_responder_ping(chat_id, context.args[0], context)
#         return

#     context.user_data["esperando_ip"] = True
#     await context.bot.send_message(chat_id=chat_id, parse_mode="HTML", text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe la IP o Host a verificar.")

# async def texto_libre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return

#     if context.user_data.get("esperando_ip"):
#         context.user_data["esperando_ip"] = False
#         await procesar_y_responder_ping(chat_id, update.message.text.strip(), context)
#     else:
#         await context.bot.send_message(chat_id=chat_id, text="⚠️ Comando no reconocido. Usa /start para abrir el panel.", parse_mode="HTML")

# async def procesar_y_responder_ping(chat_id, host, context):
#     msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"🔄 Ejecutando ICMP hacia {host}...")
#     ok, lat = await hacer_ping_async(host, ETH2_IP)
#     msg_res = f"📡 <b>RESULTADO PING MANUAL</b>\n<b>Destino:</b> <code>{host}</code>\n" + (f"<b>Estado:</b> ✅ OK\n<b>Latencia:</b> {lat} ms" if ok else "<b>Estado:</b> ❌ SIN RESPUESTA")
#     await context.bot.edit_message_text(chat_id=chat_id, message_id=msg_wait.message_id, text=msg_res, parse_mode='HTML')
#     await enviar_panel_principal(context, chat_id)

# async def dhcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return
#     context.user_data["esperando_ip"] = False
    
#     puede, s = verificar_cooldown(chat_id, "run_dhcp", 30)
#     if not puede:
#         await update.message.reply_text(f"⏳ El proceso DHCP se limpió hace poco. Espera {s}s.")
#         return
        
#     msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Solicitando ejecución de limpieza DHCP...")
#     await ejecutar_limpieza_dhcp(chat_id, context, msg_wait.message_id)

# async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return
#     context.user_data["esperando_ip"] = False
    
#     puede, s = verificar_cooldown(chat_id, "cmd_alertas", 3)
#     if not puede: return

#     log_path = os.path.join(os.path.dirname(__file__), "log_ejecucion.txt")
#     if not os.path.exists(log_path):
#         await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Historial de Alertas</b>\nNo se registran eventos en la bitácora local.", parse_mode="HTML")
#         return

#     try:
#         with open(log_path, "r", encoding="utf-8") as f:
#             lineas = f.readlines()
#         if not lineas:
#             await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Historial de Alertas</b>\nBitácora vacía.", parse_mode="HTML")
#             return
        
#         ultimos_logs = [l.strip() for l in lineas[-8:]]
#         texto_logs = "\n".join(ultimos_logs)
#         msg = f"📋 <b>Últimos Eventos y Alertas (Red/Core)</b>\n<pre>{texto_logs}</pre>"
#     except Exception as e:
#         msg = f"❌ <b>Error al leer logs:</b>\n<code>{str(e)}</code>"
        
#     await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")

# async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     chat_id = update.effective_chat.id
#     if not is_allowed_chat(chat_id): return
#     context.user_data["esperando_ip"] = False
#     msg = (
#         "⚙️ <b>Centro de Soporte Sentinela</b>\n\n"
#         "• <code>/start</code> - Inicializa la matriz de botones.\n"
#         "• <code>/status [sector]</code> - Escanea sectores.\n"
#         "• <code>/ping</code> - Pide IP en el siguiente input.\n"
#         "• <code>/dhcp</code> - Ejecuta liberación core.pyw.\n"
#         "• <code>/alertas</code> - Lee el log de fallos y core."
#     )
#     await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")

# # ===============================================
# # PROCESADOR DE BOTONES (CALLBACKS BLINDADO)
# # ===============================================
# async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     chat_id = query.message.chat_id
    
#     if not is_allowed_chat(chat_id):
#         await query.answer("🚫 No tienes permisos de TI para usar este bot.", show_alert=True)
#         return
        
#     data = query.data

#     if data in ["scan_all", "run_dhcp"]:
#         puede, s = verificar_cooldown(chat_id, data, segundos_espera=30)
#         if not puede:
#             await query.answer(f"⏳ Acción protegida. Por favor, espera {s}s para evitar saturación.", show_alert=True)
#             return

#     await query.answer()

#     if data == "scan_all":
#         context.user_data["esperando_ip"] = False
#         msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando diagnóstico general en paralelo...")
#         await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", msg_wait.message_id)
        
#     elif data.startswith("scan_"):
#         context.user_data["esperando_ip"] = False
#         segmento = data.split("_")[1]
#         msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"⏳ Evaluando segmento físico: {segmento.upper()}...")
#         await ejecutar_escaneo_segmento(chat_id, context, segmento, f"REPORTE SECTORIAL: {segmento.upper()}", msg_wait.message_id)
        
#     elif data == "menu_status":
#         context.user_data["esperando_ip"] = False
#         keyboard = [
#             [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
#             [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"), InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
#             [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
#         ]
#         await context.bot.send_message(chat_id=chat_id, text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona el segmento de red:", parse_mode="HTML", markup=InlineKeyboardMarkup(keyboard))

#     elif data == "solicitar_ping":
#         context.user_data["esperando_ip"] = True
#         await context.bot.send_message(chat_id=chat_id, text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe la IP o el Host a testear:", parse_mode='HTML')

#     elif data == "run_dhcp":
#         context.user_data["esperando_ip"] = False
#         msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Solicitando ejecución de limpieza DHCP...")
#         await ejecutar_limpieza_dhcp(chat_id, context, msg_wait.message_id)

# # ===============================================
# # RUTINAS OPERATIVAS AUXILIARES
# # ===============================================
# async def ejecutar_escaneo_segmento(chat_id, context, segmento, titulo, message_id):
#     if segmento == "all": items_a_revisar = NETWORK_TARGETS
#     else: items_a_revisar = CATEGORIAS.get(segmento, {})

#     if not items_a_revisar: return

#     tareas = [check_single_target(nom, t, dir) for nom, (t, dir) in items_a_revisar.items()]
#     resultados = await asyncio.gather(*tareas)
    
#     cuerpo = [f"🌐 <b>{titulo}</b>", f"<i>Origen: {ETH2_IP or 'Default'}</i>\n"] + resultados

#     # --- ESCRITURA DINÁMICA DE ALERTAS POR DESCONEXIÓN ---
#     log_path = os.path.join(os.path.dirname(__file__), "log_ejecucion.txt")
#     lineas_fallidas = []
#     ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     for res in resultados:
#         if "❌" in res:
#             texto_plano = res.replace("• ", "").replace("<b>", "").replace("</b>", "")
#             lineas_fallidas.append(f"[{ahora_str}] ALERTA: {texto_plano}\n")
            
#     if lineas_fallidas:
#         try:
#             with open(log_path, "a", encoding="utf-8") as f:
#                 f.writelines(lineas_fallidas)
#         except Exception as e:
#             print(f"Error al escribir en log: {e}")

#     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\n".join(cuerpo), parse_mode='HTML')
#     await enviar_panel_principal(context, chat_id)

# async def ejecutar_limpieza_dhcp(chat_id, context, message_id):
#     script_path = os.path.join(os.path.dirname(__file__), "core.pyw")
#     if not os.path.exists(script_path):
#         await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ <b>Error:</b> No se encontró <code>core.pyw</code>.", parse_mode="HTML")
#         return

#     try:
#         def _run_script():
#             res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=15)
#             return res.returncode
#         await asyncio.to_thread(_run_script)
#         msg_final = "🧹 <b>Mantenimiento DHCP Ejecutado</b>\nLas IPs redundantes en el Core han sido liberadas con éxito."
#     except Exception as e:
#         msg_final = f"❌ <b>Fallo al lanzar core.pyw:</b>\n<code>{str(e)}</code>"

#     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg_final, parse_mode="HTML")
#     await enviar_panel_principal(context, chat_id)

# def main():
#     app = ApplicationBuilder().token(TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("status", status))
#     app.add_handler(CommandHandler("ping", ping_custom))
#     app.add_handler(CommandHandler("dhcp", dhcp))
#     app.add_handler(CommandHandler("alertas", alertas))
#     app.add_handler(CommandHandler("ayuda", ayuda))
#     app.add_handler(CallbackQueryHandler(callback_router))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_libre_handler))

#     print("✅ Servidor Sentinela acoplado con HUD interactivo, Control de Saturación y Logs Integrados.")
#     app.run_polling(poll_interval=1)

# if __name__ == "__main__":
#     main()





import asyncio
import os
import subprocess
import sys
import time
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import psutil
import httpx
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

# CATEGORIAS = {
#     "servidores": {
#         "INTERNET 8.8.8.8": ("PING", "8.8.8.8"),
#         "SERVIDOR_Dominio": ("PING", "172.19.1.151"),
#         "SERVIDOR_Dominio2": ("PING", "172.19.1.1"),
#         "SERVIDOR_Files": ("PING", "172.19.1.110"),
#         "SERVIDOR_SIU": ("PING", "172.19.1.105"),
#         "SERVIDOR_PRUEBA": ("PING", "172.19.1.220"),
#         "SERVIDOR_ZKBIO": ("PING", "172.19.1.121"),
#         "SERVIDOR_PRUEBA_GERARDO": ("PING", "172.19.1.210"),
#         "HTTP-105": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
#         "HTTP-106": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
#     },
#     "switch": {
#         "SWITCH_CORE": ("PING", "172.19.1.254"),
#         "SWITCH_INFORMATICA_PISO1_1": ("PING", "172.19.1.2"),
#         "SWITCH_INFORMATICA_PISO1_2": ("PING", "172.19.1.3"),
#         "SWITCH_INFORMATICA_PISO2_1": ("PING", "172.19.1.4"),
#         "SWITCH_INFORMATICA_PISO2_2": ("PING", "172.19.1.5"),
#         "SWITCH_INFORMATICA_PISO3_1": ("PING", "172.19.1.6"),
#         "SWITCH_INFORMATICA_PISO3_2": ("PING", "172.19.1.7"),
#         "SWITCH_GOBIERNO": ("PING", "172.19.1.31"),
#         "SWITCH_BIBLIOTECA": ("PING", "172.19.1.14"),
#         "SWITCH_RECTORADO": ("PING", "172.19.1.17"),
#         "SWITCH_PABA_PISO1_1": ("PING", "172.19.1.12"),
#         "SWITCH_PABA_PISO2_1": ("PING", "172.19.1.13"),
#         "SWITCH_PABB_PISO1": ("PING", "172.19.1.25"),
#         "SWITCH_PABB_PISO2": ("PING", "172.19.1.26"),
#         "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED": ("PING", "172.19.1.16"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_1": ("PING", "172.19.1.19"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_2": ("PING", "172.19.1.27"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_3": ("PING", "172.19.1.29"),
#         "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED": ("PING", "172.19.1.28"),
#         "SWITCH_FIA_PISO1_1": ("PING", "172.19.1.253"),
#         "SWITCH_FIA_PISO1_2": ("PING", "172.19.1.33"),
#         "SWITCH_FIA_PISO3_1": ("PING", "172.19.1.43"),
#         "SWITCH_FIA_A": ("PING", "172.19.1.45"),
#         "SWITCH_FIA_B": ("PING", "172.19.1.34"),
#     },
#     "biometricos": {
#         "MOLINETE_SALIDA": ("PING", "172.19.1.196"),
#         "MOLINETE_INGRESO": ("PING", "172.19.1.195"),
#         "BIOMETRICO_CIENCIASSALUD": ("PING", "172.19.1.200"),
#         "BIOMETRICO_FIA": ("PING", "172.19.1.202"),
#         "BIOMETRICO_PABELLON-B": ("PING", "172.19.1.201"),
#         "BIOMETRICO_PABELLON-A": ("PING", "172.19.1.199"),
#         "BIOMETRICO_RECEPCION-BALTA": ("PING", "172.26.5.38"),
#         "BIOMETRICO_INFORMATICA": ("PING", "172.19.1.198"),
#         "BIOMETRICO_AdminPradera": ("PING", "172.19.1.197"),
#         "BIOMETRICO_AdminBalta": ("PING", "172.26.5.37"),
#     }
# }
CATEGORIAS = {
    "servidores": {
        "INTERNET (8.8.8.8)": ("PING", "8.8.8.8"),
        "SERVIDOR_Dominio (172.19.1.151)": ("PING", "172.19.1.151"),
        "SERVIDOR_Dominio2 (172.19.1.1)": ("PING", "172.19.1.1"),
        "SERVIDOR_Files (172.19.1.110)": ("PING", "172.19.1.110"),
        "SERVIDOR_SIU (172.19.1.105)": ("PING", "172.19.1.105"),
        "SERVIDOR_PRUEBA (172.19.1.220)": ("PING", "172.19.1.220"),
        "SERVIDOR_ZKBIO (172.19.1.121)": ("PING", "172.19.1.121"),
        "SERVIDOR_PRUEBA_GERARDO (172.19.1.210)": ("PING", "172.19.1.210"),
        "HTTP-105 (172.19.1.105)": ("HTTP", "http://172.19.1.105/SIU/publico/inicioSesion.jsp"),
        "HTTP-106 (172.19.1.106)": ("HTTP", "http://172.19.1.106/SIU/publico/inicioSesion.jsp"),
    },
    "switch": {
        "SWITCH_CORE (172.19.1.254)": ("PING", "172.19.1.254"),
        "SWITCH_INFORMATICA_PISO1_1 (172.19.1.2)": ("PING", "172.19.1.2"),
        "SWITCH_INFORMATICA_PISO1_2 (172.19.1.3)": ("PING", "172.19.1.3"),
        "SWITCH_INFORMATICA_PISO2_1 (172.19.1.4)": ("PING", "172.19.1.4"),
        "SWITCH_INFORMATICA_PISO2_2 (172.19.1.5)": ("PING", "172.19.1.5"),
        "SWITCH_INFORMATICA_PISO3_1 (172.19.1.6)": ("PING", "172.19.1.6"),
        "SWITCH_INFORMATICA_PISO3_2 (172.19.1.7)": ("PING", "172.19.1.7"),
        "SWITCH_GOBIERNO (172.19.1.31)": ("PING", "172.19.1.31"),
        "SWITCH_BIBLIOTECA (172.19.1.14)": ("PING", "172.19.1.14"),
        "SWITCH_RECTORADO (172.19.1.17)": ("PING", "172.19.1.17"),
        "SWITCH_PABA_PISO1_1 (172.19.1.12)": ("PING", "172.19.1.12"),
        "SWITCH_PABA_PISO2_1 (172.19.1.13)": ("PING", "172.19.1.13"),
        "SWITCH_PABB_PISO1 (172.19.1.25)": ("PING", "172.19.1.25"),
        "SWITCH_PABB_PISO2 (172.19.1.26)": ("PING", "172.19.1.26"),
        "SWITCH_CIENCIASDELASALUD_PISO1_1_PARED (172.19.1.16)": ("PING", "172.19.1.16"),
        "SWITCH_CIENCIASDELASALUD_PISO2_1 (172.19.1.19)": ("PING", "172.19.1.19"),
        "SWITCH_CIENCIASDELASALUD_PISO2_2 (172.19.1.27)": ("PING", "172.19.1.27"),
        "SWITCH_CIENCIASDELASALUD_PISO2_3 (172.19.1.29)": ("PING", "172.19.1.29"),
        "SWITCH_CIENCIASDELASALUD_PISO2_4_PARED (172.19.1.28)": ("PING", "172.19.1.28"),
        "SWITCH_FIA_PISO1_1 (172.19.1.253)": ("PING", "172.19.1.253"),
        "SWITCH_FIA_PISO1_2 (172.19.1.33)": ("PING", "172.19.1.33"),
        "SWITCH_FIA_PISO1_3 (172.19.1.46)": ("PING", "172.19.1.46"),
        "SWITCH_FIA_PISO3_1 (172.19.1.43)": ("PING", "172.19.1.43"),
        "SWITCH_FIA_A (172.19.1.45)": ("PING", "172.19.1.45"),
        "SWITCH_FIA_B (172.19.1.34)": ("PING", "172.19.1.34"),
    },
    "biometricos": {
        "MOLINETE_SALIDA (172.19.1.196)": ("PING", "172.19.1.196"),
        "MOLINETE_INGRESO (172.19.1.195)": ("PING", "172.19.1.195"),
        "BIOMETRICO_CIENCIASSALUD (172.19.1.200)": ("PING", "172.19.1.200"),
        "BIOMETRICO_FIA (172.19.1.202)": ("PING", "172.19.1.202"),
        "BIOMETRICO_PABELLON-B (172.19.1.201)": ("PING", "172.19.1.201"),
        "BIOMETRICO_PABELLON-A (172.19.1.199)": ("PING", "172.19.1.199"),
        "BIOMETRICO_RECEPCION-BALTA (172.26.5.38)": ("PING", "172.26.5.38"),
        "BIOMETRICO_INFORMATICA (172.19.1.198)": ("PING", "172.19.1.198"),
        "BIOMETRICO_AdminPradera (172.19.1.197)": ("PING", "172.19.1.197"),
        "BIOMETRICO_AdminBalta (172.26.5.37)": ("PING", "172.26.5.37"),
    }
}
NETWORK_TARGETS = {}
for data_cat in CATEGORIAS.values():
    NETWORK_TARGETS.update(data_cat)

# ===============================================
# FILTRO DE SEGURIDAD Y COOLDOWNS
# ===============================================
raw_users = os.getenv("USERS_PERMITIDOS", "")
USUARIOS_AUTORIZADOS = [int(uid.strip()) for uid in raw_users.split(",") if uid.strip()]
IDS_PERMITIDOS = [CHAT_GRUPAL_PERMITIDO] + USUARIOS_AUTORIZADOS

def is_allowed_chat(chat_id: int) -> bool:
    return chat_id in IDS_PERMITIDOS

COOLDOWNS = {}

def verificar_cooldown(id_clave: int, tipo_accion: str, segundos_espera: int) -> tuple[bool, int]:
    ahora = time.time()
    if id_clave not in COOLDOWNS:
        COOLDOWNS[id_clave] = {}
    ultima_vez = COOLDOWNS[id_clave].get(tipo_accion, 0)
    tiempo_transcurrido = ahora - ultima_vez
    if tiempo_transcurrido < segundos_espera:
        return False, int(segundos_espera - tiempo_transcurrido)
    COOLDOWNS[id_clave][tipo_accion] = ahora
    return True, 0

# ===============================================
# CORE DE VERIFICACIÓN ASÍNCRONA
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

async def check_single_target(nombre, tipo, direccion):
    if tipo == "PING":
        ok, lat = await hacer_ping_async(direccion, ETH2_IP)
        estado = f"• <b>{nombre}</b>: ✅ OK ({lat} ms)" if ok else f"• <b>{nombre}</b>: ❌ CAÍDO"
    else:
        ok, info = await probar_http_async(direccion)
        estado = f"• <b>{nombre}</b>: ✅ OK ({info})" if ok else f"• <b>{nombre}</b>: ❌ ERROR ({info})"
    return estado

# ===============================================
# FUNCIÓN REUTILIZABLE PARA EL PANEL (CON ALERTAS Y AYUDA)
# ===============================================
async def enviar_panel_principal(context, chat_id):
    keyboard = [
        [InlineKeyboardButton("📊 Diagnóstico Completo", callback_data="scan_all")],
        [InlineKeyboardButton("📁 Ver por Categorías", callback_data="menu_status")],
        [InlineKeyboardButton("📡 Lanzar Ping Manual", callback_data="solicitar_ping"),
         InlineKeyboardButton("🧹 Liberar DHCP", callback_data="run_dhcp")],
        [InlineKeyboardButton("📋 Ver Alertas Recientes", callback_data="ver_alertas"),
         InlineKeyboardButton("❓ Guía / Ayuda", callback_data="ver_ayuda")]
    ]
    await context.bot.send_message(
        chat_id=chat_id, parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard),
        text=f"🛰️ <b>Sentinela Bot — Panel de Control</b>\nIP Origen: <code>{ETH2_IP or 'Default'}</code>\n\nPresiona una opción del tablero o usa el menú nativo."
    )

# ===============================================
# MANEJADORES DE COMANDOS (HUD)
# ===============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    context.user_data["esperando_ip"] = False
    await enviar_panel_principal(context, chat_id)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    context.user_data["esperando_ip"] = False

    if context.args:
        objetivo = context.args[0].lower()
        if objetivo in ["all", "todos"]:
            puede, s = verificar_cooldown(chat_id, "scan_all", 30)
            if not puede:
                await update.message.reply_text(f"⏳ Espera {s}s para un nuevo diagnóstico masivo.")
                return
            msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando diagnóstico general...")
            await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", msg_wait.message_id)
            return
        elif objetivo in CATEGORIAS:
            msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"⏳ Evaluando {objetivo.upper()}...")
            await ejecutar_escaneo_segmento(chat_id, context, objetivo, f"REPORTE SECTORIAL: {objetivo.upper()}", msg_wait.message_id)
            return
        else:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Sector inválido. Usa: `all`, `switch`, `biometricos` o `servidores`.", parse_mode="Markdown")
            return

    keyboard = [
        [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
        [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"), InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
        [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
    ]
    await context.bot.send_message(
        chat_id=chat_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard),
        text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona qué segmento de red deseas resolver:"
    )

async def ping_custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return

    if context.args:
        context.user_data["esperando_ip"] = False
        await procesar_y_responder_ping(chat_id, context.args[0], context)
        return

    context.user_data["esperando_ip"] = True
    await context.bot.send_message(chat_id=chat_id, parse_mode="HTML", text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe la IP o Host a verificar.")

async def texto_libre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return

    if context.user_data.get("esperando_ip"):
        context.user_data["esperando_ip"] = False
        await procesar_y_responder_ping(chat_id, update.message.text.strip(), context)
    else:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Comando no reconocido. Usa /start para abrir el panel.", parse_mode="HTML")

async def procesar_y_responder_ping(chat_id, host, context):
    msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"🔄 Ejecutando ICMP hacia {host}...")
    ok, lat = await hacer_ping_async(host, ETH2_IP)
    msg_res = f"📡 <b>RESULTADO PING MANUAL</b>\n<b>Destino:</b> <code>{host}</code>\n" + (f"<b>Estado:</b> ✅ OK\n<b>Latencia:</b> {lat} ms" if ok else "<b>Estado:</b> ❌ SIN RESPUESTA")
    await context.bot.edit_message_text(chat_id=chat_id, message_id=msg_wait.message_id, text=msg_res, parse_mode='HTML')
    await enviar_panel_principal(context, chat_id)

async def dhcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    context.user_data["esperando_ip"] = False
    
    puede, s = verificar_cooldown(chat_id, "run_dhcp", 30)
    if not puede:
        await update.message.reply_text(f"⏳ El proceso DHCP se limpió hace poco. Espera {s}s.")
        return
        
    msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Solicitando ejecución de limpieza DHCP...")
    await ejecutar_limpieza_dhcp(chat_id, context, msg_wait.message_id)

async def alertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    context.user_data["esperando_ip"] = False
    
    puede, s = verificar_cooldown(chat_id, "cmd_alertas", 3)
    if not puede: return
    await ejecutar_lectura_alertas(chat_id, context)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not is_allowed_chat(chat_id): return
    context.user_data["esperando_ip"] = False
    await ejecutar_envio_ayuda(chat_id, context)

# ===============================================
# PROCESADOR DE BOTONES (CALLBACKS BLINDADO)
# ===============================================
async def callback_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    
    if not is_allowed_chat(chat_id):
        await query.answer("🚫 No tienes permisos de TI para usar este bot.", show_alert=True)
        return
        
    data = query.data

    if data in ["scan_all", "run_dhcp"]:
        puede, s = verificar_cooldown(chat_id, data, segundos_espera=30)
        if not puede:
            await query.answer(f"⏳ Acción protegida. Por favor, espera {s}s para evitar saturación.", show_alert=True)
            return

    await query.answer()

    if data == "scan_all":
        context.user_data["esperando_ip"] = False
        msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Procesando diagnóstico general en paralelo...")
        await ejecutar_escaneo_segmento(chat_id, context, "all", "REPORTE GENERAL DE RED", msg_wait.message_id)
        
    elif data.startswith("scan_"):
        context.user_data["esperando_ip"] = False
        segmento = data.split("_")[1]
        msg_wait = await context.bot.send_message(chat_id=chat_id, text=f"⏳ Evaluando segmento físico: {segmento.upper()}...")
        await ejecutar_escaneo_segmento(chat_id, context, segmento, f"REPORTE SECTORIAL: {segmento.upper()}", msg_wait.message_id)
        
    elif data == "menu_status":
        context.user_data["esperando_ip"] = False
        keyboard = [
            [InlineKeyboardButton("⚡ TODO", callback_data="scan_all")],
            [InlineKeyboardButton("🖥️ SERVIDORES", callback_data="scan_servidores"), InlineKeyboardButton("🔌 SWITCHES", callback_data="scan_switch")],
            [InlineKeyboardButton("👣 BIOMÉTRICOS", callback_data="scan_biometricos")]
        ]
        # CORREGIDO: Se cambió 'markup=' por 'reply_markup=' para solucionar el TypeError
        await context.bot.send_message(chat_id=chat_id, text="📊 <b>Módulo de Diagnóstico</b>\nSelecciona el segmento de red:", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "solicitar_ping":
        context.user_data["esperando_ip"] = True
        await context.bot.send_message(chat_id=chat_id, text="📝 <b>Modo Ping Activado</b>\nPor favor, escribe la IP o el Host a testear:", parse_mode='HTML')

    elif data == "run_dhcp":
        context.user_data["esperando_ip"] = False
        msg_wait = await context.bot.send_message(chat_id=chat_id, text="⏳ Solicitando ejecución de limpieza DHCP...")
        await ejecutar_limpieza_dhcp(chat_id, context, msg_wait.message_id)
        
    elif data == "ver_alertas":
        context.user_data["esperando_ip"] = False
        await ejecutar_lectura_alertas(chat_id, context)
        
    elif data == "ver_ayuda":
        context.user_data["esperando_ip"] = False
        await ejecutar_envio_ayuda(chat_id, context)

# ===============================================
# RUTINAS OPERATIVAS AUXILIARES
# ===============================================
async def ejecutar_escaneo_segmento(chat_id, context, segmento, titulo, message_id):
    if segmento == "all": items_a_revisar = NETWORK_TARGETS
    else: items_a_revisar = CATEGORIAS.get(segmento, {})

    if not items_a_revisar: return

    tareas = [check_single_target(nom, t, dir) for nom, (t, dir) in items_a_revisar.items()]
    resultados = await asyncio.gather(*tareas)
    
    cuerpo = [f"🌐 <b>{titulo}</b>", f"<i>Origen: {ETH2_IP or 'Default'}</i>\n"] + resultados

    # --- ESCRITURA DINÁMICA DE ALERTAS POR DESCONEXIÓN ---
    log_path = os.path.join(os.path.dirname(__file__), "log_ejecucion.txt")
    lineas_fallidas = []
    ahora_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for res in resultados:
        if "❌" in res:
            texto_plano = res.replace("• ", "").replace("<b>", "").replace("</b>", "")
            lineas_fallidas.append(f"[{ahora_str}] ALERTA: {texto_plano}\n")
            
    if lineas_fallidas:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.writelines(lineas_fallidas)
        except Exception as e:
            print(f"Error al escribir en log: {e}")

    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\n".join(cuerpo), parse_mode='HTML')
    await enviar_panel_principal(context, chat_id)

async def ejecutar_limpieza_dhcp(chat_id, context, message_id):
    script_path = os.path.join(os.path.dirname(__file__), "core.pyw")
    if not os.path.exists(script_path):
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ <b>Error:</b> No se encontró <code>core.pyw</code>.", parse_mode="HTML")
        return

    try:
        def _run_script():
            res = subprocess.run([sys.executable, script_path], capture_output=True, text=True, timeout=15)
            return res.returncode
        await asyncio.to_thread(_run_script)
        msg_final = "🧹 <b>Mantenimiento DHCP Ejecutado</b>\nLas IPs redundantes en el Core han sido liberadas con éxito."
    except Exception as e:
        msg_final = f"❌ <b>Fallo al lanzar core.pyw:</b>\n<code>{str(e)}</code>"

    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=msg_final, parse_mode="HTML")
    await enviar_panel_principal(context, chat_id)

async def ejecutar_lectura_alertas(chat_id, context):
    log_path = os.path.join(os.path.dirname(__file__), "log_ejecucion.txt")
    if not os.path.exists(log_path):
        await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Historial de Alertas</b>\nNo se registran eventos en la bitácora local.", parse_mode="HTML")
        await enviar_panel_principal(context, chat_id) # <--- AGREGADO AQUÍ
        return

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        if not lineas:
            await context.bot.send_message(chat_id=chat_id, text="🔔 <b>Historial de Alertas</b>\nBitácora vacía.", parse_mode="HTML")
            await enviar_panel_principal(context, chat_id) # <--- AGREGADO AQUÍ
            return
        
        ultimos_logs = [l.strip() for l in lineas[-8:]]
        texto_logs = "\n".join(ultimos_logs)
        msg = f"📋 <b>Últimos Eventos y Alertas (Red/Core)</b>\n<pre>{texto_logs}</pre>"
    except Exception as e:
        msg = f"❌ <b>Error al leer logs:</b>\n<code>{str(e)}</code>"
        
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
    await enviar_panel_principal(context, chat_id) # <--- AGREGADO AQUÍ

async def ejecutar_envio_ayuda(chat_id, context):
    msg = (
        "⚙️ <b>Centro de Soporte Sentinela</b>\n\n"
        "• <code>/start</code> - Inicializa la matriz de botones.\n"
        "• <code>/status [sector]</code> - Escanea sectores.\n"
        "• <code>/ping</code> - Pide IP en el siguiente input.\n"
        "• <code>/dhcp</code> - Ejecuta liberación core.pyw.\n"
        "• <code>/alertas</code> - Lee el log de fallos y core."
    )
    await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")
    await enviar_panel_principal(context, chat_id) # <--- AGREGADO AQUÍ

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("ping", ping_custom))
    app.add_handler(CommandHandler("dhcp", dhcp))
    app.add_handler(CommandHandler("alertas", alertas))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CallbackQueryHandler(callback_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_libre_handler))

    print("✅ Servidor Sentinela acoplado con HUD interactivo, Control de Saturación y Logs Integrados.")
    app.run_polling(poll_interval=1)

if __name__ == "__main__":
    main()