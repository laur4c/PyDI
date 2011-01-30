import logging
import libxml2
import container
 
class XmlConfigParser:
    
    configFile = None
    
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
            
        except IndexError as exception:
            raise container.ConfigParserBeanNotFoundException(exception)

        #initialize bean definition
        bean = container.BeanDefinition()
        bean.set_id(id)
        bean.set_fullname(xmlNode.prop("fullname"))
        
        #iterates node childs of bean tag          
        arguments = None
        properties = None
        aspects = None

        for child in xmlNode.children:
                
            if child.parent.name == "init" and child.name == "arg":
                if arguments is None:
                    arguments = []
                arguments.append(self.fetch_argument(child))

            elif child.name == "property":   
                if properties is None:
                    properties = []
                properties.append(self.fetch_property(child))
                
            elif child.name == "aspect":
                if aspects is None:
                    aspects = []
                aspects.append(self.fetch_aspect(child))
            
        bean.set_init_arguments(arguments)
        bean.set_properties(properties)
        bean.set_aspects(aspects)
        
        context.xpathFreeContext()
       
        return bean
        
    def fetch_argument(self, node):        
        arg = container.ArgumentBeanDefinition()
        
        child = node.children
        while child is not None:
                        
            if child.type == "element":
                arg.set_type("bean")                
                arg.set_value(child.prop("bean"))
                       
            elif child.type == "text":
                arg.set_type("plain")
                arg.set_value(child.content)
            
            child = child.next

        return arg
        
    def fetch_property(self, node):
        property = container.PropertyBeanDefinition()
        property.set_name(node.prop("name"))

        child = node.children
        while child is not None:           
            if child.type == "element":                
                property.set_type("bean")            
                property.set_value(child.prop("bean"))                
                
            child = child.next
         
        if property.get_value() is None:
            property.set_type("plain")
            property.set_value(node.content);
        
        return property

    def fetch_aspect(self, node):
        aspect = container.AspectBeanDefinition()
        aspect.set_bean(node.prop("ref"))
        
        pointcuts = []
        child = node.children
        while child is not None:
            if child.name == "pointcut":
                pointcuts.append(child.prop("method"))
            
            child = child.next

        if len(pointcuts) is not 0:
            aspect.set_pointcuts(pointcuts)
            return aspect
            
        raise container.AspectBeanDefinitionException(
            "aspect pointcuts must be defined"
        )
            
        














