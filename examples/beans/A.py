class A:
    a = None
    
    def __init__(self):
        print "init...."
    
    def a_method(self, arg1, arg2):
        print "executing a method..."
        print arg1, arg2
        return "Return value"
        
    def b_method(self):
        print "executing b method..."    
    
    def c_method(self):
        print "c"