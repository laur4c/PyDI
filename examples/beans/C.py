from pydi import aspect

class C(aspect.AbstractAspect):
    
    def invoke(self, methodInvocation):
        print "do something before proceed"
        
        methodInvocation.proceed()
        
        print methodInvocation.returnValue
        print "do something after proceed"
       
    
    
    