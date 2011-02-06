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

from BeanFactory import BeanFactory
from providers import XMLProvider

import logging
import logging.config

class Container:
    
    options = None
    logger = None     
    factory = None

    def __init__(self, options):
        self.options = options
        logging.config.fileConfig(self.options['log_conf'])
        self.logger = logging.getLogger("appLogging")        

    def get_factory(self):        
        if isinstance(self.factory, BeanFactory):
            return self.factory
        
        provider = XMLProvider(self.options)
        
        factory = BeanFactory()
        factory.set_provider(provider)
        self.factory = factory
        
        return factory

    def get_bean(self, id):
        return self.get_factory().get_bean(id)
    
