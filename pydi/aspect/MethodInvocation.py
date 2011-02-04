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

class MethodInvocation(object):
    """
    An instance of this class will be passed as argument
    to all defined aspects 
    """   
    def __init__(self):
        self._args = None
        self._pointcut = None
        self._target = None
        self._advice = None
        self._joinpoint = None
        self._returnValue = None
    
    def get_arguments(self):
        """Arguments passed to aspected method"""
        return self._args
    
    def set_arguments(self, value):
        self._args = value
    
    def get_target(self):
        """Object advised by aspects"""
        return self._target
    
    def set_target(self, value):
        self._target = value
        
    def get_joinpoint(self):
        """This is the method to intercept"""
        return self._joinpoint
    
    def set_joinpoint(self, value):
        self._joinpoint = value
        
    def get_advice(self):
        """
        This method must be defined in an aspect class.
        It is a implementation of the "invoke" method 
        (see AbstractAspect abstract base class)
        """
        return self._advice
    
    def set_advice(self, value):
        self._advice = value
    
    def get_pointcut(self):        
        return self._pointcut
    
    def set_pointcut(self, value):
        self._pointcut = value
        
    def get_return_value(self):
        return self._returnValue
    
    def set_return_value(self, value):
        self._returnValue = value
    
    def proceed(self):
        """Execution of the original method and store returned value"""
        self._returnValue = self._joinpoint(self._target, *self._args)    
    
    joinpoint = property(get_joinpoint, set_joinpoint)
    args = property(get_arguments, set_arguments)
    target = property(get_target, set_target)
    advice = property(get_advice, set_advice)
    pointcut = property(get_pointcut, set_pointcut)
    returnValue = property(get_return_value, set_return_value)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    