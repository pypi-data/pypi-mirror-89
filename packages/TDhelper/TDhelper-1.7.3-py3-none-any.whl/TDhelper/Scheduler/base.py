
class Scheduler():
    def __init__(self,name,plug,taskType="interval",startTime=None,sleep=0):
        """Init task
            params:
                name: str
                plug:call task module
                taskType:task type
                    realtime:run at now
                    interval:loop run and sleep N millisecond,default value
                    timing:run at one datetime
                startTime:first run time
                sleep:sleep millisecond
        """
        self.__config={
        'name':name,
        'plug':plug,
        'type':taskType,#realtime,interval,timing
        'starttime':startTime,
        'sleep':sleep,#millisecond;
    }

    def Config(self):
        return self.__config
