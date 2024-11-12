import paramiko
import time

# Archivos
ip_file = 'ips.txt'         
user_file = 'usuarios.txt'  


old_password = 'Ww234fcsQ$'  # Contraseña actual del usuario
new_password = 'Ww234fcsQ$123'        # Nueva contraseña intermedia
final_password = '$BNCtec13'

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
        time.sleep(1)

        
        shell.send('sys\n')
        time.sleep(1)

        shell.send(f'aaa\n')
        time.sleep(1)

        shell.send(f'local-user {username} password irreversible-cipher {new_password}\n')
        time.sleep(1)

        shell.send(f'{old_password}\n')
        time.sleep(1)

        shell.send('y\n')
        time.sleep(1)

        shell.send('q\n')
        time.sleep(1) 
        shell.send('q\n')
        time.sleep(1)

        shell.send('save\n')
        time.sleep(1)

        shell.send('y\n')
        time.sleep(1)     

        client.close()



        print(f'Nueva conexion a {ip} para cambiar contraseña de {username}...')
        #Aplicaremos los cambios
        client.connect(ip, username=username, password=new_password)
        time.sleep(1) 
        shell.send('y\n')
        time.sleep(1) 
        shell.send('{old_password}\n')
        time.sleep(1) 
        shell.send('{final_password}\n')
        time.sleep(1)
        shell.send('{final_password}\n')
        time.sleep(1) 
        print(f'Cambio realizado para la ip {ip} con el usuario {username} la contraseña es: {final_password}')

        # Leer la salida de los comandos
        output = shell.recv(65535).decode('utf-8')
        print(f'Salida de {ip} para {username}:\n{output}')
        

    except Exception as e:
        print(f'Error al conectar o cambiar contraseña en {ip} para {username}: {e}')
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
