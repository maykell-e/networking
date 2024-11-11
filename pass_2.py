import paramiko
import time

# Archivos
ip_file = 'ips.txt'         # Archivo con las direcciones IP de los dispositivos
user_file = 'usuarios.txt'  # Archivo con los nombres de usuarios

# Credenciales
old_password = 'WFT234xd555$'  # Contraseña actual del usuario
new_password = 'WFTsdc5$'        # Nueva contraseña

def change_password(ip, username):
    client = paramiko.SSHClient()
    try:
        # Establecer política para claves de host desconocidas
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conectar al dispositivo utilizando SSH
        print(f'Conectando a {ip} para cambiar contraseña de {username}...')
        client.connect(ip, username=username, password=old_password)

        # Abrir un shell interactivo
        shell = client.invoke_shell()

        # Esperar a que se cargue la shell
        time.sleep(1)

        # Enviar los comandos para entrar al modo de configuración
        shell.send('sys\n')
        time.sleep(1)  # Esperar un poco para que el modo se active

        shell.send(f'aaa\n')
        time.sleep(1)        

        # Cambiar la contraseña del usuario actual
        shell.send(f'local-user {username} password irreversible-cipher {new_password}\n')
        time.sleep(1)
        

        shell.send(f'{old_password}\n')
        time.sleep(1)
        

        # Guardar la configuración
        shell.send('save\n')
        time.sleep(1)
       

        # Confirmar el guardado
        shell.send('y\n')
        time.sleep(1)
      

        # Leer la salida de los comandos
        output = shell.recv(65535).decode('utf-8')
        print(f'Salida de {ip} para {username}:\n{output}')
        

    except Exception as e:
        print(f'Error al conectar o cambiar contraseña en {ip} para {username}: {e}')
        print ("echo no lo hace")
    finally:
        # Cerrar la conexión SSH después de cada sesión
        client.close()
        print(f'Conexión cerrada con {ip} para {username}')


# Leer las IPs desde el archivo
with open(ip_file, 'r') as file:
    ips = file.read().strip().split(',')

# Leer los usuarios desde el archivo
with open(user_file, 'r') as file:
    users = file.read().strip().split(',')

# Cambiar la contraseña en cada dispositivo y para cada usuario de forma secuencial
for ip in ips:
    for user in users:
        change_password(ip.strip(), user.strip())
