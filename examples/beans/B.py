class B:
    
    property = None
    bean = None
    
    def __init__(self, db, host, user, passwd, bean):
        print db, host, user, passwd, bean
    
    def set_property(self, value):
        self.property = value

    def get_property(self):
        return self.property
    
    def set_bean(self, value):
        self.bean = value
        
    def get_bean(self):
        return self.bean