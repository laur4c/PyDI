# -*- coding: utf-8 -*-
# Copyright (c) 2011 Laura Corvalán <corvalan.laura@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import aspect

import inspect
import re
import logging

class BeanFactory:
    
    provider = None
    logger = None
        
    # created beans cache
    cache = {}    

    def __init__(self):        
        self.logger = logging.getLogger("appLogging")  
        
    def set_provider(self, value):
        self.provider = value
    
    def store(self, id, bean):
        if id in self.cache:
            return

        self.cache[id] = bean
        
    def is_created(self, id):
        if id in self.cache:
            return True
        return False
    
    def ask_for_bean(self, id):
        if self.is_created(id):
            return self.cache[id]
        
        return False
        
    def get_bean(self, id):
        
        created = self.ask_for_bean(id)
        if created is not False:
            return created
        
        descriptor = self.provider.get_bean_definition(id)            
                
        # define arguments
        args = self.get_arguments(descriptor.get_init_arguments())
        
        # create bean
        bean = self.create_proxy(
            descriptor.get_fullname(), 
            args, 
            descriptor.get_aspects()
        )
        
        # define properties
        self.set_properties(bean, descriptor.get_properties())
        
        self.store(id, bean)
        return bean
    
    def get_arguments(self, metadata):
        args = ()
        
        if metadata is None:
            return None

        for arg in metadata:
            value = arg.get_value()
            
            if arg.get_type() == "bean":
                args += self.get_bean(value),                                
            else:
                args += value,

        return args

    def set_properties(self, bean, metadata):
        if metadata is None:
            return 

        for property in metadata:            
            name = property.get_name()
            value = property.get_value()
                
            if property.get_type() == "bean":
                value = self.get_bean(value)
                
            try:
                method = getattr(bean, "set_" + name)
                method(value)
                    
            except AttributeError as e:
                self.logger.debug("no setter found for property " + name)
                bean = None
                raise e

    def create_proxy(self, fullname, args = None, aspectsDef = None):
        module = __import__(fullname)
        
        list = fullname.split(".")
        bean = list.pop()
        
        proxy = getattr(module, bean)                
        self.decorate(proxy, aspectsDef)
        
        if args:
            return proxy(*args)
        else:            
            return proxy()
    
    def decorate(self, proxy, metadata):
        """aspecting methods...."""
        
        if metadata is None:
            return
        
        for descriptor in metadata:
            aspect = self.get_bean(descriptor.get_bean())
            advice = getattr(aspect, "interceptor")
            
            for pointcut in descriptor.get_pointcuts():
                self.apply_aspect(proxy, advice, pointcut)
                
    def apply_aspect(self, proxy, advice, pointcut):
        joinpoints = self.find_joinpoints(proxy, pointcut)
        
        for joinpoint in joinpoints:
            
            methodInvocation = aspect.MethodInvocation()
            methodInvocation.pointcut = joinpoint
            
            method = getattr(proxy, joinpoint)
            setattr(proxy, joinpoint, advice(method, methodInvocation))
        
    def find_joinpoints(self, proxy, pointcut):        
        retval = []
                
        if pointcut in proxy.__dict__:
            retval.append(pointcut)
            return retval
                
        members = inspect.getmembers(proxy)
        for name, obj in members:            
            if inspect.ismethod(obj) is False:
                continue
            
            if re.search(pointcut, name) is not None:
                retval.append(name)
        
        return retval
            
            
            
                
        
        
        
    
