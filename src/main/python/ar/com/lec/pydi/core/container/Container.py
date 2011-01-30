import configuration
import container
import logging
from xml.dom import minidom
import imp

class Container:
    
    logger = None 
    configIni = None
    factory = None

    def __init__(self, inifile, env):
        self.configIni = configuration.ConfigIni(inifile, env)
        
        self.logger = logging.getLogger("appLogging")
        self.logger.debug(inifile) 

    def get_factory(self):

        if isinstance(self.factory, container.BeanFactory):
            return self.factory

        provider = container.XmlConfigParser(self.configIni.pathContainer)
        
        factory = container.BeanFactory()
        factory.set_provider(provider)
        self.factory = factory
        
        return factory

    def get_bean(self, id):
        return self.get_factory().get_bean(id)
    
