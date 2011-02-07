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

import pickle
import os.path

class Cache(object):
    """ File cache """
    
    class __CacheImpl():
        directory = None
            
        def set_directory(self, value):
            self.directory = value
            
        def has(self, name):
            if os.path.isfile(self.directory + "/" + name):
                return True  
            return False
        
        def store(self, name, value):            
            file = open(self.directory + "/" + name, "w")
            pickle.dump(value, file, -1)
            file.close()
            
        def fetch(self, name):            
            file = open(self.directory + "/" + name, "r")            
            retval = pickle.load(file)
            file.close()
            
            return retval
                        
    __instance = None
    
    def __init__(self, options=None):
        # already instantiated
        if Cache.__instance is None:            
            Cache.__instance = Cache.__CacheImpl()
            Cache.__instance.set_directory(options['cache_directory'])
        
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)

    
    
  
    
    