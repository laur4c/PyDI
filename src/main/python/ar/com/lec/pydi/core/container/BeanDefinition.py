class BeanDefinition:
    
    id = None
    fullname = None
    
    #A collection of PropertyBeanDefinition objects
    properties = None
    
    #A collection of ArgumentBeanDefinition objects
    initArguments = None
        
    def set_id(self, value):
        self.id = value

    def get_id(self):
        return self.id
    
    def set_fullname(self, value):
        self.fullname = value
        
    def get_fullname(self):
        return self.fullname
    
    def set_properties(self, value):
        self.properties = value
        
    def get_properties(self):
        return self.properties
    
    def set_init_arguments(self, value):
        self.initArguments = value
        
    def get_init_arguments(self):
        return self.initArguments