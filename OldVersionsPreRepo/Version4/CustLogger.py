"""
This file creates a logging system for our BackUp process.
Yes, I know Python has a built in logging library, but I'm building this from scratch because I'm trying to learn programming.
So, I figured creating a simple logging class will teach me valuable stuff.
"""

"""
What
"""
import os
import datetime

class CustLogger:
    def __init__(self,LogLocation):
        self.LogLocation = LogLocation
        self.DateFormat = "%Y-%m-%d %H:%M:%S.%f"
        # self.FileDateFormat = '%Y_%m_%d'
        self.LogDate = datetime.datetime.now().date()
        self.LogDirs = ["debug","info","error"]

    def InitLogDir(self):
        """
        Here we check the log directory to ensure the relevant directories are created.
        For the most part, nothing should happen. Only the initial execution of the library should create the log directory

        Future Idea... we can make this function create our log directory instead of us specifying the location. Would probably make things easier as we don't have to specify it in our main script
        """
        for directory in self.LogDirs:
            if not os.path.exists(os.path.join(self.LogLocation,directory)):
                os.makedirs(os.path.join(self.LogLocation,directory))
            else:
                continue
        
        return None
        

    def debug(self,message):
        now = datetime.datetime.now()
        CurrentTimestamp = now.strftime(self.DateFormat)
        DebugFile = os.path.join(self.LogLocation,"debug",f"{self.LogDate}_debug.txt")
        if os.path.isfile(DebugFile):
            with open(DebugFile,'a') as file:
                file.write(f"\n{CurrentTimestamp} - {message}")
            return None
        else:
            with open(DebugFile,'w') as file:
                file.write(f"{CurrentTimestamp} - {message}")
                return None
        # return DebugFile

    def error(self,message):
        now = datetime.datetime.now()
        CurrentTimestamp = now.strftime(self.DateFormat)
        ErrorFile = os.path.join(self.LogLocation,"error",f"{self.LogDate}_error.txt")
        if os.path.isfile(ErrorFile):
            with open(ErrorFile,'a') as file:
                file.write(f"\n{CurrentTimestamp} - {message}")
            return None
        else:
            with open(ErrorFile,'w') as file:
                file.write(f"{CurrentTimestamp} - {message}")
                return None
        # return ErrorFile

    def info(self,message):
        now = datetime.datetime.now()
        CurrentTimestamp = now.strftime(self.DateFormat)
        InfoFile = os.path.join(self.LogLocation,"info",f"{self.LogDate}_info.txt")
        if os.path.isfile(InfoFile):
            with open(InfoFile,'a') as file:
                file.write(f"\n{CurrentTimestamp} - {message}")
            return None
        else:
            with open(InfoFile,'w') as file:
                file.write(f"{CurrentTimestamp} - {message}")
                return None
        # return infoFile

    # Can create a general log() function that takes the log type as input
    # We will use this method if all the logs have the exact same message written. Otherwise, I'll personalize as needed.
    # Again, for now we'll have four methods, but we can delete debug/error/info above if needed
    def log(self, type: str, Message: str,isPrint: bool = False):
        if type not in self.LogDirs:
            raise ValueError(f"Invalid log type: {type}. Allowed types are {self.LogDirs}")

        now = datetime.datetime.now()
        CurrentTimestamp = now.strftime(self.DateFormat)
        LogType = type.lower()
        LogFile = os.path.join(self.LogLocation,LogType,f"{self.LogDate}_{LogType}.txt")
        if os.path.isfile(LogFile):
            with open(LogFile,'a') as file:
                file.write(f"\n{CurrentTimestamp} - {Message}")
            # return None
        else:
            with open(LogFile,'w') as file:
                file.write(f"\n{CurrentTimestamp} - {Message}")
            # return None
        
        if isPrint:
            print(Message)

        return None


## Below is for Testing...
# CurrentDir = os.getcwd()
# Location = os.path.join(CurrentDir,'log')

# logger = CustLogger(LogLocation=Location)

# Debug = logger.debug(message="testing debug")
# Error = logger.error(message="testing error")
# Info = logger.info(message="testing info")

# logger.log(Message="testing log method for debug",type="debug")
# logger.log(Message="testing log method for info",type="info",isPrint=True)
# logger.log(Message="testing log method for info",type="inffo")
