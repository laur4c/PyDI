import configuration
import container
import logging
from xml.dom import minidom
import imp

class Container:
    
    logger = None 
    configIni = None
    mapper = None
    
    def __init__(self, inifile, env):
        self.configIni = configuration.ConfigIni(inifile, env)
        
        self.logger = logging.getLogger("appLogging")
        self.logger.debug(inifile) 
        
        
    def get_bean(self, id):
        provider = container.XmlConfigParser(self.configIni.pathContainer)
        factory = BeanFactory(provider)
        return factory.get_bean(id)
    
    def load(self):
       
        a = container.XmlConfigParser(self.configIni.pathContainer)
        b = a.get_bean_definition("BBean")
        
        print b
        
        dom = minidom.parse(self.configIni.pathContainer)
        #move this to get_bean method, using lazy pattern and avoid
        #load all beans when load container
        #And load only the requested bean
        
        self.mapper = self.map_beans(dom)        
        
    def map_beans(self, dom):
        beans = {}
        for node in dom.getElementsByTagName("bean"):            
            id = node.getAttribute("id")
            
            arguments = None            
            for init in node.getElementsByTagName("init"):
                
                for element in init.childNodes:
                    if arguments is None:
                        arguments = ()
                        
                    if element.localName == "arg":
                        arguments += element.firstChild.data,
                    elif element.localName == "ref":
                        arguments += element.getAttribute("bean"),
                
            #see for properties 
            properties = None            
            for child in node.getElementsByTagName("property"):
                
                if properties is None:
                    properties = {}
                    properties["beans"], properties["values"] = {}, {}
                        
                propertyName = child.getAttribute("name")
                if child.getElementsByTagName("ref").__len__() == 0:
                    properties["values"] = {
                        "name" : propertyName, 
                        "value" : child.firstChild.data
                    }
                else:
                    for ref in child.getElementsByTagName("ref"):            
                        if ref.hasAttribute("bean"):
                            beanName = ref.getAttribute("bean")                   
                            properties["beans"] = {
                                "name" : propertyName,
                                "bean" : beanName
                            }
                
            #adds the bean to mapper 
            beans[id] = {
                "id": id,
                "name": node.getAttribute("fullname"),
            }
            
            if arguments:                
                beans[id]["initArgs"] = arguments
            
            if properties:
                beans[id]["properties"] = properties 
        
        return beans
    
    def get_bean_(self, id):
        objConfig = self.mapper[id]
        
        args = None
        if "initArgs" in objConfig:            
            args = objConfig["initArgs"]
        
        print objConfig["initArgs"]
        bean = self.instantiate(objConfig["name"], args)
        
        if "properties" in objConfig:
            for ref, propertyMap in objConfig["properties"].iteritems():
                
                propertyName = propertyMap["name"]
                
                if ref == "values":                    
                    propertyValue = propertyMap["value"]
                elif ref == "beans":
                    beanID = propertyMap["bean"]
                    
                    if beanID in self.mapper:
                        
                        config = self.mapper[beanID]                        
                        route = config["name"]
                        propertyValue = self.instantiate(route)
                    else:
                        raise Exception("not found any bean")
                                         
                try:
                    method = getattr(bean, "set_" + propertyName)
                    method(propertyValue)
                
                except AttributeError as e:
                    self.logger.debug(
                        "no setter found for property " + propertyName 
                        + " of " + id + " class"
                    )
                    raise e
                            
        return bean
    
    def instantiate(self, bean, args = None):
        module = __import__(bean)
        
        list = bean.split(".")
        component = list.pop()
        
        attr = getattr(module, component)                
                
        if args:
            return attr(*args)
        else:
            return attr()
    
    
    