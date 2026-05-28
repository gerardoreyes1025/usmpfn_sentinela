import os
from datetime import datetime
from netmiko import ConnectHandler

# Configuración del dispositivo core
core_device = {
    'device_type': 'cisco_ios_telnet',
    'host': '172.19.1.254',               # Tu IP
    'username': 'admin',            # Tu Usuario
    'password': 'ibmcisco',        # Tu Contraseña
    'port': 23,
    'secret': 'ibmcisco',    # Tu Enable (si aplica, si no déjalo en '')
}

# Obtener la fecha y hora actual para el reporte
ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    # Conexión y ejecución silenciosa
    net_connect = ConnectHandler(**core_device)
    
    if core_device['secret']:
        net_connect.enable()
    
    # Ejecución de los comandos
    net_connect.send_command('clear ip dhcp binding *')
    net_connect.send_command('clear ip dhcp conflict *')
    
    net_connect.disconnect()
    
    # Registro de éxito en el archivo de logs
    with open("log_ejecucion.txt", "a", encoding="utf-8") as f:
        f.write(f"[{ahora}] ÉXITO: Tablas de DHCP limpiadas correctamente.\n")

except Exception as e:
    # Registro de errores en el mismo archivo para centralizar todo
    with open("log_ejecucion.txt", "a", encoding="utf-8") as f:
        f.write(f"[{ahora}] ERROR: No se pudo ejecutar la limpieza. Motivo: {str(e)}\n")