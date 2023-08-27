import configparser as parser
from apscheduler.schedulers.background import BackgroundScheduler
import json

class ControlplaneService:
    def __init__(self, ControlplaneDao, DataAggrService):
        self.ControlplaneDao = ControlplaneDao
        self.DataAggrService = DataAggrService

        self.sched = BackgroundScheduler()
        self.sched.start()
    
        properties = parser.ConfigParser()
        properties.read('./config/application.ini')
        service_config = properties['SERVICE']
        self.service_config=service_config

    def aggrJobList(self):
        schedules = []
        for job in self.sched.get_jobs():
            jobId=job.id
            schedules.append(jobId)
        resultList=schedules
        return resultList
        
    def humTemperEnable(self):
        if (self.service_config['USE_HUM_TEMPER'] == "True"):
            try:
                self.sched.add_job(self.DataAggrService.humTemperDataSend, 'interval', seconds=5, id="humTemper", replace_existing=True)
                return "Enable Module for Humid&Temperature"
            except :
                return "Add Job Internal Error"
        else : return "This Module is unavailable"

    def npkEnable(self):
        if (self.service_config['USE_NPK'] == "True"):
            try:
                self.sched.add_job(self.DataAggrService.npkDataSend, 'interval', seconds=5, id="npk", replace_existing=True)
                return "Enable Module for NPK"
            except :
                return "Add Job Internal Error"
        else : return "This Module is unavailable"
        
    def humTemperDisable(self):
        if (self.service_config['USE_HUM_TEMPER'] == "True"):
            try:
                self.sched.remove_job("humTemper")
                return "Disable Module for Humid&Temperature"
            except :
                return "Module for Humid&Temperature is not Enabled"
        else : return "This Module is unavailable"

    def npkDisable(self):
        if (self.service_config['USE_NPK'] == "True"):
            try:
                self.sched.remove_job("npk")
                return "Disable Module for NPK"
            except :
                return "Module for Humid&Temperature is not Enabled"
        else : return "This Module is unavailable"


        
    