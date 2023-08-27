
import sys
from app            import create_app
from flask_twisted  import Twisted
from twisted.python import log

config_path = sys.argv[1]

if __name__ == '__main__':
    app = create_app(config_path)
    
    twisted = Twisted(app)
    log.startLogging(sys.stdout)

    app.logger.info(f"Running the app...")
    app.run(debug=True, host='0.0.0.0', port=5003)