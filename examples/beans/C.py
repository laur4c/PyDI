import container

class C(container.AbstractAspect):
    
    def invoke(self, methodInvocation):
        print "do something before proceed"
        
        methodInvocation.proceed()
        
        print methodInvocation.returnValue
        print "do something after proceed"
       
    
    
    