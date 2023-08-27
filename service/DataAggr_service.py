import configparser as parser
import json
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient

class DataAggrService:
    def __init__(self, DataAggrDao, influxDbUrl, influxDbToken, influxDbBucket, influxDbOrg, kafkaProducer):
        self.DataAggrDao = DataAggrDao
        self.influxDbUrl = influxDbUrl
        self.influxDbToken = influxDbToken
        self.influxDbBucket = influxDbBucket
        self.influxDbOrg = influxDbOrg
        self.kafkaProducer = kafkaProducer

        properties = parser.ConfigParser()
        properties.read('./config/application.ini')
        service_config = properties['SERVICE']
        self.service_config=service_config

    def locationCheck(self):
        result = {"LOCATION" : "LOCATION_VALUE"}
        return result

    def humTemperDataSend(self):
        influxDbClient=InfluxDBClient(url=self.influxDbUrl, token=self.influxDbToken, org=self.influxDbOrg)
        sensorData = self.DataAggrDao.checkHumTemSensor()
        if sensorData['Humidity'] is not None and sensorData['Temperature'] is not None:
            # print(self.service_config['APP_KEY'])
            send2InfluxData = ["%s,host=%s temperature=%f" % (self.service_config['GROUP_ID'], self.service_config['DEVICE_ID'], sensorData['Temperature']), "%s,host=%s humid=%f" % (self.service_config['GROUP_ID'],self.service_config['DEVICE_ID'], sensorData['Humidity'])]
            # send2InfluxData = ["jpkim_home,host=raspberrypi temperature=%f" % (sensorData['Temperature']), "jpkim_home,host=raspberrypi humid=%f" % (sensorData['Humidity'])]
            
            # print(send2InfluxData)
            write_api = influxDbClient.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.influxDbBucket, self.influxDbOrg, send2InfluxData)
            influxDbClient.close()

            send2KafkaData = {'Humidity':sensorData['Humidity'], 'Temperature':sensorData['Temperature']}
            send2KafkaKey = {'GroupID':int(self.service_config['GROUP_ID']),'DeviceID': int(self.service_config['DEVICE_ID'])}
            print('SendData Key :',send2KafkaKey,'to Kafka Server :',send2KafkaData) 
            self.kafkaProducer.send('soildata', key=json.dumps(send2KafkaKey).encode('utf-8'), value=send2KafkaData)
            self.kafkaProducer.flush()
        
    def npkDataSend(self):
        influxDbClient=InfluxDBClient(url=self.influxDbUrl, token=self.influxDbToken, org=self.influxDbOrg)
        sensorData = self.DataAggrDao.checkNpkSensor()
        if sensorData['Nitrogen'] is not None and sensorData['Phosphorus'] is not None and sensorData['Potassium'] is not None:
            send2InfluxData = ["jpkim_home,host=%s Nitrogen=%f" % (self.service_config['DEVICE_ID'], sensorData['Nitrogen']), "jpkim_home,host=%s Phosphorus=%f" % (self.service_config['DEVICE_ID'], sensorData['Phosphorus']), "jpkim_home,host=%s Potassium=%f" % (self.service_config['DEVICE_ID'], sensorData['Potassium'])]
            write_api = influxDbClient.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.influxDbBucket, self.influxDbOrg, send2InfluxData)
            influxDbClient.close()
    



