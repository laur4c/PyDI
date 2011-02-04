class A:
    a = "A"
    b = "B"
    
    def __init__(self):
        print "init"
    
    def get_property_a(self, arg1, arg2):
        print "executing method..."
        print arg1, arg2
        return self.a
        
    def get_property_b(self):
        print "executing method..."
        return self.b    
    
    def prefix_a(self):
        print "executing method..."
    
    def prefix_b(self):
        print "executing method..."
        
    def prefix_c(self):
        print "executing method..."