# SMURF의 Endpoint용 에이전트
- Sensor Data Aggregation
- 서버에서 요청하는 Endpoint Status, Information 응답

# 실행방법 : 
1) 집에서
DataAggrDao에서 아래 주석
    -# import Adafruit_DHT as dht
    -# hum,temper =dht.read_retry(dht.DHT11,4)
python run.py .\config\profileDevHome.py

2) 서버에서
python3 run.py ./config/profileDevEndpoint.py
