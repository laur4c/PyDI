class ArgumentBeanDefinition:
    
    #Expected values: plain or bean
    type = None
    value = None
    
    def set_type(self, value):
        self.type = value
        
    def get_type(self):
        return self.type
    
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value