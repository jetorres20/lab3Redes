import socket
import time
import hashlib
import threading
import logging
import select


def recibir():
    time.sleep(1)
    msg, address = s.recvfrom(1024)
    msg= msg.decode("Latin1")
    if len(msg)==0:
        return True
    global opcion
    string = "Recibido de: "+str(address) + " El mensaje:    "+ msg 
    print(string)
    return False

def enviar(add, string):
    time.sleep(1)
    msg = string
    s.sendto(bytes(msg, "Latin1"),add)
    print("Enviado a:  " + str(add[0]) + " El mensaje:    "+ msg)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def confirmacion(add):
    print("Entré a confirmación")
    time.sleep(2)
    enviar(add,"OK")
    print("Tiempo actual: " + time.strftime("%H:%M:%S", time.localtime()))
    s.settimeout(4)
    try:
        msg,add = s.recvfrom(1024)
        msg= msg.decode("Latin1")
        print("Message from Client:{}".format(msg))
        if msg =="OK":
            print("El cliente " + str(add)+ " recibió el mensaje correctamente")
            logging.debug("El cliente " + str(add)+ " recibió el mensaje correctamente")
        else:
            print("El cliente " + str(add)+ " no recibió el mensaje correctamente")
            logging.debug("El cliente " + str(add)+ " no recibió el mensaje correctamente")
    except Exception:
        print("No se recibió confirmación del cliente.")
        logging.debug("No se recibió confirmación del cliente.")
        s.settimeout(None)

    print("Gracias, por todo!")
   
def enviar_archivo_eleccion( address):
    b.wait()
    logging.debug("El cliente tiene la ip: " + str(address))
    if opcion == "1":
        logging.debug("Se enviará archivo 1. Tamaño: 100MB")
        enviarHash( address, 1)
        print("Enviando paquetes...")
        enviarArchivo100( address)
    if opcion == "2":
        logging.debug("Se enviará archivo 2. Tamaño: 250MB")
        enviarHash( address, 2)
        while recibir( ):
            pass
        print("Enviando paquetes...")
        enviarArchivo250( address)

def enviarHash(add, archive):
    if archive == 1:
        fil = open('100Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(add, hashcode.decode("Latin1"))
        fil.close()
    if archive == 2:
        fil = open('250Mb.mp4','rb')
        hashcode = sha2(fil.read())
        enviar(add, hashcode.decode("Latin1"))
        fil.close()

def enviarArchivo100(add):
    contadorPaquetes = 0
    video = open('100Mb.mp4','rb')
    logging.debug("El nombre del archivo es 100Mb.mp4")
    logging.debug("Tiempo actual: " + time.strftime('%d-%m-%Y-%H:%M:%S' , time.localtime()))
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(1024)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        s.sendto(buff,add)
        buff = video.read(1024)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    logging.debug("Los paquetes enviados fueron: " + str(contadorPaquetes))
    logging.debug("El tiempo de transferencia fue: " + str(tiempoEnvio)) 
    print("Envío completado.")
    print("Tiempo de envío: " + str(tiempoEnvio) + " Segundos.")

def enviarArchivo250(add):
    contadorPaquetes = 0
    video = open('250Mb.mp4','rb')
    logging.debug("El nombre del archivo es 250Mb.mp4")
    logging.debug("Tiempo actual: " + time.strftime('%d-%m-%Y-%H:%M:%S', time.localtime()))
    print('Enviando paquetes a ',str(add[0]),'...')
    buff = video.read(1024)
    inicio = time.time()
    while (buff):
        contadorPaquetes += 1
        s.sendto(buff,add)
        buff = video.read(1024)
    video.close()
    fin = time.time()
    tiempoEnvio = fin - inicio
    logging.debug("Los paquetes enviados fueron: " + str(contadorPaquetes))
    logging.debug("El tiempo de transferencia fue: " + str(tiempoEnvio)) 
    print("Envío completado.")
    print("Tiempo de envío: " + str(tiempoEnvio) + " Segundos.")

def atenderCliente(data, add):
    mensaje = data.decode("Latin1")
    clientMsg = "Message from Client:{}".format(mensaje)
    clientIP  = "Client IP Address:{}".format(add)
    print(clientMsg)
    print(clientIP)
    enviar_archivo_eleccion(add)
    confirmacion(add)
    


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((socket.gethostname(), 65000))
opcion = 0
n=0   
logging.basicConfig(filename='tmp.log',
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    level=logging.DEBUG) 
n =  int(input ("¿A cuántos clientes quiere atender hoy?"))
opcion = input("Seleccione la opción del archivo que quiere enviar hoy: \n1. Archivo 100 Mib\n2. Archivo 250 MiB\n--->")   
b = threading.Barrier(n)
    
def wait_for_client(s):

        try:
            while True: # keep alive

                try: # receive request from client
                    data, client_address = s.recvfrom(1024)
                    if data.decode("Latin1") == "Hola.Estoy preparado para recibir datos.":
                        c_thread = threading.Thread(target = atenderCliente,
                                                args = (data, client_address))
                        c_thread.daemon = True
                        c_thread.start()

                except OSError as err:
                    print(err)

        except KeyboardInterrupt:
            s.close()


wait_for_client(s)
#while True:
#    t = threading.Thread(target = atenderCliente)
#    t.start()




