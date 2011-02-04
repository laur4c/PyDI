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

class BeanDefinition:
    
    id = None
    fullname = None
    
    #A collection of PropertyBeanDefinition objects
    properties = None
    
    #A collection of ArgumentBeanDefinition objects
    initArguments = None
    
    #A collection of AspectBeanDefinition objects
    aspects = None
        
    def set_id(self, value):
        self.id = value

    def get_id(self):
        return self.id
    
    def set_fullname(self, value):
        self.fullname = value
        
    def get_fullname(self):
        return self.fullname
    
    def set_properties(self, value):
        self.properties = value
        
    def get_properties(self):
        return self.properties
    
    def set_init_arguments(self, value):
        self.initArguments = value
        
    def get_init_arguments(self):
        return self.initArguments
    
    def set_aspects(self, value):
        self.aspects = value
        
    def get_aspects(self):
        return self.aspects