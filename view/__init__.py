from flask      import request, jsonify, current_app, Response, g
from flask.json import JSONEncoder

def create_endpoints(app, services):
    app.json_encoder = JSONEncoder

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"
    
    @app.route('/findLocation', methods=['GET'])
    def findLocation():
        return jsonify({'location' : services.ControlplaneService.locationCheck()})
    
    @app.route('/listJob', methods=['GET'])
    def listJob():
        return jsonify({'schedule_jobs' : services.ControlplaneService.aggrJobList()})
    
    @app.route('/enableJob/humTemper', methods=['GET'])
    def enableJobHumTemper():
        return services.ControlplaneService.humTemperEnable()

    @app.route('/enableJob/npk', methods=['GET'])
    def enableJobNpk():
        return services.ControlplaneService.npkEnable()
    
    @app.route('/disableJob/humTemper', methods=['GET'])
    def disableJobHumTemper():
        return services.ControlplaneService.humTemperDisable()

    @app.route('/disableJob/npk', methods=['GET'])
    def disableJobNpk():
        return services.ControlplaneService.npkDisable()