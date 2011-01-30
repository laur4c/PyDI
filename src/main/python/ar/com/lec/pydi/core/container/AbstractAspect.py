from abc import ABCMeta, abstractmethod

class AbstractAspect:
    __metaclass__ = ABCMeta
        
    def interceptor(self, func, methodInvocation):
        methodInvocation.advice = self.invoke
        methodInvocation.joinpoint = func
            
        def wrapper(self, *args):
            methodInvocation.args = args
            methodInvocation.target = self
                        
            methodInvocation.advice(methodInvocation)        
        
        return wrapper
    
    @abstractmethod    
    def invoke(self):     
        """ advice """
    
