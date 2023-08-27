from config.default import *

db = {
    'user'     : 'root',
    'password' : 'password',
    'host'     : 'localhost',
    'port'     : 3306,
    'database' : 'iotdb'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
KAFKA_BROKER = f"0.0.0.0:9092"