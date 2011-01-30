class AspectBeanDefinition:
    
    bean = None
    pointcuts = []
    
    def set_bean(self, value):
        self.bean = value
        
    def get_bean(self):
        return self.bean
    
    def set_pointcuts(self, value):
        self.pointcuts = value
        
    def get_pointcuts(self):
        return self.pointcuts