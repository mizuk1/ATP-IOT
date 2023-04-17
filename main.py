import urequests
import time
import dht
import machine
import network

#função que realiza a conexão a rede WIFI
def conecta(ssid, senha):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, senha)
    for t in range(50):
        if station.isconnected():
            break
        time.sleep(0.1)
    return station

print("Conectando...")
station = conecta("USUÁRIO", "SENHA")
if not station.isconnected():
    print("Não conectado!...")
else:
    print("Conectado!...")
    d = dht.DHT11(machine.Pin(4))
    r = machine.Pin(2, machine.Pin.OUT)
    while True:
        print("\nRealizando medições...")
        d.measure()
        if(d.temperature() > 31 or d.humidity() > 70):
            r.value(1) #liga o rele
        else:
            r.value(0) #desliga o rele
        print("Temp={} Umid={}".format(d.temperature(), d.humidity()))
        print("Acessando o site...")
        response = urequests.get("https://api.thingspeak.com/update?api_key=AKAOD9NQ9JF64ORR&field1="+str(d.temperature())+"&field2="+str(d.humidity()))
        print("Informação enviada!")
        response.close()
        time.sleep(15)
    station.disconnect()