# import Adafruit_DHT as dht
import datetime


class DataAggrDao:
    def __init__(self, database):
        self.db = database

    def checkLocationSensor(self):
        result = {}
        return result
    
    def checkHumTemSensor(self):
        # hum,temper =dht.read_retry(dht.DHT11,4)
        hum = 64
        temper = 23.1
        print("Temperature = {1:0.1f}*C Humidity = {2:0.1f}%".format(datetime.datetime.now(), temper,  hum))
        result = {"Temperature":temper, "Humidity":hum}
        return result

    def checkNpkSensor(self):
        # 센서 측정
        n = 20
        p = 20
        k = 20
        print("Nitrogen = {1:0.1f} Phosphorus = {2:0.1f} Potassium = {3:0.1f}".format(datetime.datetime.now(), n,  p, k))
        result = {"Nitrogen":n, "Phosphorus":p, "Potassium":k}
        return result
