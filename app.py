
from flask 		import Flask
from sqlalchemy	import create_engine
from kafka 		import KafkaConsumer, KafkaAdminClient, KafkaProducer
from json       import dumps
from flask_cors import CORS

from view		import create_endpoints
from model		import *
from service	import *


class Services:
    pass

class Models:
    pass

###################################################################
# Create APP
###################################################################
	
def create_app(config_path):
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile(config_path)

    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    
    kafkaBroker=app.config['KAFKA_BROKER']
    kafkaProducer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=kafkaBroker, value_serializer=lambda x: dumps(x).encode('utf-8'))

    influxDbUrl = app.config['INFLUXDB_URL']
    influxDbToken = app.config['INFLUXDB_TOKEN']
    influxDbBucket = app.config['INFLUXDB_BUCKET']
    influxDbOrg = app.config['INFLUXDB_ORG']

    print("KAFKA BROKER ADDRESS is "+kafkaBroker)
    print("INFLUXDB information is "+influxDbUrl)
    # kafkaConsumer = KafkaConsumer(bootstrap_servers=kafkaBroker)
    # kafkaAdminClient = KafkaAdminClient(bootstrap_servers=kafkaBroker)

	## Persistence Layer
    model = Models
    model.ControlplaneDao = ControlplaneDao(database)
    model.DataAggrDao = DataAggrDao(database)
	
	## Business Layer
    services = Services
    services.DataAggrService = DataAggrService(model.DataAggrDao, influxDbUrl, influxDbToken,influxDbBucket, influxDbOrg, kafkaProducer)
    services.ControlplaneService = ControlplaneService(model.ControlplaneDao, services.DataAggrService)
    
	## 엔드포인트 생성		
    create_endpoints(app, services)

    return app