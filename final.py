import paramiko
import time

# Archivo de configuración
user_file = 'usuarios.txt'
intermediate_password = '23$sCrsc2'  # Contraseña intermedia
final_password = '$BNCtNCtec$342'     # Contraseña definitiva

def change_password(ip, username, old_password):
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Establecer política para claves de host desconocidas

        print(f'[INFO] Conectando a {ip} para cambiar contraseña de {username}...')
        client.connect(ip, username=username, password=old_password)
        print (f'print old password {old_password}')

        shell = client.invoke_shell()  # Abrir un shell interactivo
        time.sleep(1)  # Esperar a que se cargue la shell

        # Cambiar a modo de configuración
        shell.send('sys\n')
        time.sleep(2)
        shell.send('aaa\n')
        time.sleep(2)

        # Cambiar la contraseña a la contraseña intermedia
        shell.send(f'local-user {username} password irreversible-cipher {intermediate_password}\n')
        print (f'Passsword intermedio {intermediate_password}')
        time.sleep(2)
        shell.send(f'{old_password}\n')  # Confirmar con la contraseña antigua
        time.sleep(1)

        # Guardar la configuración
        shell.send('return\n')
        time.sleep(1)        

        shell.send('save\n')
        time.sleep(1)

        shell.send('y\n')  # Confirmar el guardado
        time.sleep(2)

        # Leer la salida de los comandos
        output = shell.recv(65535).decode('utf-8')
        print(f'[INFO] Salida de {ip} para {username} (cambio a contraseña intermedia):\n{output}')
    except Exception as e:
        print(f'[ERROR] Error al conectar o cambiar contraseña intermedia en {ip} para {username}: {e}')
    finally:
        try:
            client.close()
        except:
            pass
        print(f'[INFO] Conexión cerrada con {ip} para {username}')

    # Realizar la segunda conexión para establecer la contraseña definitiva
    reconnect_and_set_final_password(ip, username)

def reconnect_and_set_final_password(ip, username):
    client = paramiko.SSHClient()
    try:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Establecer política para claves de host desconocidas

        print(f'[INFO] Reconectando a {ip} con la contraseña intermedia...')
        client.connect(ip, username=username, password=intermediate_password)
        print (f'Nueva password {intermediate_password}')

        shell = client.invoke_shell()
        time.sleep(1)

        # Cambiar la contraseña a la definitiva
        shell.send('y\n')
        time.sleep(1) 

        shell.send(f'{intermediate_password}\n')  # Confirmar con la contraseña intermedia
        time.sleep(1)

        shell.send('{final_password}\n')
        time.sleep(1)

        shell.send('{final_password}\n')
        time.sleep(1)

        shell.send('return\n')
        time.sleep(1)

        shell.send('save\n')  # guardar
        time.sleep(2)

        shell.send('y\n')  # Confirmar el guardado
        time.sleep(2)

        # Leer la salida del cambio final
        output = shell.recv(65535).decode('utf-8')
        print(f'[INFO] Salida de {ip} para {username} (cambio a contraseña definitiva):\n{output}')

        print(f'[SUCCESS] Cambio realizado para {username} en {ip}. Contraseña definitiva: {final_password}')
    except Exception as e:
        print(f'[ERROR] Error al reconectar o cambiar contraseña definitiva en {ip} para {username}: {e}')
    finally:
        try:
            client.close()
        except:
            pass
        print(f'[INFO] Conexión cerrada con {ip} para {username}')


# Leer las entradas desde el archivo usuarios.txt
try:
    with open(user_file, 'r') as file:
        users_data = file.readlines()

    print(f'[INFO] Usuarios cargados desde {user_file}: {len(users_data)} registros encontrados.')

    # Procesar cada entrada
    for entry in users_data:
        # Separar los datos por ":"
        try:
            username, old_password, ip = entry.strip().split(':')
            change_password(ip, username, old_password)
        except ValueError as ve:
            print(f'[ERROR] Formato inválido en la línea: {entry.strip()} - {ve}')
except FileNotFoundError:
    print(f'[ERROR] No se encontró el archivo {user_file}.')
except Exception as e:
    print(f'[ERROR] Ocurrió un error inesperado: {e}')
