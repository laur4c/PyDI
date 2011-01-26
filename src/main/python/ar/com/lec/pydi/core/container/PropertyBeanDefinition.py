class PropertyBeanDefinition:
    
    #Expected values: plain or bean
    type = None
    name = None
    value = None
    
    def set_type(self, value):
        self.type = value
        
    def get_type(self):
        return self.type
    
    def set_name(self, value):
        self.name = value
        
    def get_name(self):
        return self.name

    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value