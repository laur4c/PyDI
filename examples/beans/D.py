import container

class D(container.AbstractAspect):
    
    def invoke(self, methodInvocation):
        print "---------------------------"
        
        methodInvocation.proceed()
        
        print methodInvocation.returnValue
        print "---------------------------"
       
    
    
    