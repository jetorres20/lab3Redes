import socket
import time
import hashlib
import select

def recibir(hashvalue):
    time.sleep(1)
    if hashvalue == True:
        data = s.recv(1024)
        if len(data) == 0:
            return True
        msg = data.decode("Latin1")
        global hashcode
        hashcode = msg[5:]
        complete = "Recibido:   " + msg
        print(complete)
        return False
    else:
        data, client_address = s.recvfrom(1024)
        if len(data) == 0:
            return True
        msg = data.decode("Latin1")
        complete = "Recibido:   " + msg
        print(complete)
        return False

def enviar(string, tupla):
    time.sleep(1)
    s.send(bytes(string, "Latin1"))
    string = "Enviado:    " + string
    print(string)

def sha2(message):
    m = hashlib.sha256()
    m.update(message)
    return m.digest()

def recibirArchivo():
    s.settimeout(1.0)
    video = open('video.mp4','wb')
    inicio = time.time()
    print("Recibiendo paquetes...")
    buff, add = s.recvfrom(1024)
    try:
        while (buff):
            video.write(buff)
            buff, add = s.recvfrom(1024)
    except Exception as e:
        pass
    video.close()
    fin = time.time()
    tiempoDeTransferencia = fin - inicio - s.gettimeout()
    print("Tiempo de transferencia: " + str(tiempoDeTransferencia) + " Segundos.")
    
    
def comprobacion(tupla):
    s.settimeout(None)
    msg,add = s.recvfrom(1024)
    msg= msg.decode("Latin1")
    print("Ya lei el mensaje " + str(msg) +" del servidor en comprobacion")
    time.sleep(1)
    if str(msg)=="OK":
        video = open('video.mp4','rb')
        codigo = sha2(video.read()).decode("Latin1")
        print(codigo)
        if hashcode == codigo:
            print("Tiempo actual: " + time.strftime("%H:%M:%S", time.localtime()))
            enviar("OK", tupla)
            print("Se recibió el archivo completo y en perfecto estado.")
        else:
            print("Tiempo actual: " + time.strftime("%H:%M:%S", time.localtime()))
            enviar("FAIL", tupla)
            print("Sera necesario volver a descargar el archivo.")
        video.close()


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    #s.connect((socket.gethostname(), 65000))
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    s.connect((ip,65000))
    hashcode = b''
    
    enviar('Hola.Estoy preparado para recibir datos.', (ip,65000))
    while recibir(True):
        pass
    recibirArchivo()
    comprobacion((ip, 65000))
    print("Gracias, por todo!")

except Exception as e: 
    print("something's wrong with %s:%d. Exception is %s" % (socket.gethostname(), 65000, e))