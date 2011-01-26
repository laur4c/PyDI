import logging
import libxml2
import container
 
class XmlConfigParser:
    
    configFile = None
    properties = None
    arguments = None
    
    def __init__(self, configFile):
        self.configFile = configFile
        
    def __get_xmldoc(self):
        return libxml2.parseFile(self.configFile)
    
    
    def get_bean_definition(self, id):
        """
        Parse xml configuration and returns the bean definition
        
        @param id: ID Attribute of bean node
        @return: Bean DTO
        @rtype: BeanDefinition
        """
        
        doc = self.__get_xmldoc()        
        context = doc.xpathNewContext()
        
        try:
            # verify if bean is configured 
            xmlNode = context.xpathEval("//bean[@id='" + id + "']")
            xmlNode = xmlNode[0]
            
            #initialize bean definition
            bean = container.BeanDefinition()
            bean.set_id(id)
            bean.set_fullname(xmlNode.prop("fullname"))
            
            #iterates node childs of bean tag          
            for child in xmlNode.children:
                if child.parent.name == "init" and child.name == "arg":
                    self.add_argument(child)
                elif child.name == "property":
                    self.add_property(child)
            
            bean.set_init_arguments(self.arguments)
            bean.set_properties(self.properties)
                        
            context.xpathFreeContext()
            
        except IndexError as exception:
            raise container.ConfigParserBeanNotFoundException(exception)
        
        return bean
        
    def add_argument(self, node):        
        if self.arguments == None:
            self.arguments = []
        
        child = node.children
        while child is not None:
            arg = container.ArgumentBeanDefinition()
                        
            if child.type == "element":
                arg.set_type("bean")                
                arg.set_value(child.prop("bean"))
                       
            elif child.type == "text":
                arg.set_type("plain")
                arg.set_value(child.content)
                
            self.arguments.append(arg)
            
            child = child.next
        
    def add_property(self, node):
        if self.properties == None:
            self.properties = []
        
        child = node.children
        while child is not None:
            property = container.PropertyBeanDefinition()
            property.set_name(child.prop("name"))
                    
            if child.type == "element":
                property.set_type("bean")
                property.set_value(child.prop("bean"))
                       
            elif child.type == "text":
                property.set_type("plain")
                property.set_value(child.content)
                
            self.properties.append(property)
            
            child = child.next
            