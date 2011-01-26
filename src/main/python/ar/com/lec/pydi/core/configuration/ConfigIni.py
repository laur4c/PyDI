import ConfigParser
import logging
import logging.config

class ConfigIni:
    """Parse ini configuration file of PYDI"""
    
    pathContainer = None    
    pathLog = None
        
    def __init__(self, inifile, env):
        
        config = ConfigParser.ConfigParser()
        config.read(inifile)
                
        self.pathContainer = config.get(env, "path_container")
        self.pathLog = config.get(env, "path_log")
                
        logging.config.fileConfig(self.pathLog)        
        