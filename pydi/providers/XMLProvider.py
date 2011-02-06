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

import pydi
from pydi import definitions

import os.path
import logging
import libxml2
import memcache
import pickle
 
class XMLProvider(object):
    
    cacheEnable = None
    cacheDirectory = None
    configFile = None
    cache = {}
    
    def __init__(self, options):
        self.configFile = options['xml_file']
        self.cacheEnable = options['cache_enable']
        self.cacheDirectory = options['cache_directory']
        
    def __get_xmldoc(self):
        return libxml2.parseFile(self.configFile)
    
    
    
    def get_bean_definition(self, id):
        """
        Parse xml configuration and returns the bean definition
        
        @param id: ID Attribute of bean node
        @return: Bean DTO
        @rtype: BeanDefinition
        """
        
        if self.has_definition(id):                                             
            return self.get_loaded_definition(id)
        
        doc = self.__get_xmldoc()        
        context = doc.xpathNewContext()
        
        try:
            # verify if bean is configured 
            xmlNode = context.xpathEval("//bean[@id='" + id + "']")
            xmlNode = xmlNode[0]
            
        except IndexError as exception:
            raise pydi.providers.BeanNotFoundException(id + " bean not found ")

        #initialize bean definition
        bean = definitions.BeanDefinition()
        bean.set_id(id)
        bean.set_fullname(xmlNode.prop("fullname"))
        
        #iterates node childs of bean tag          
        arguments = None
        properties = None
        aspects = None

        for child in xmlNode.children:
                
            if child.parent.name == "init" and child.name == "arg":
                if arguments is None:
                    arguments = []
                arguments.append(self.fetch_argument(child))

            elif child.name == "property":   
                if properties is None:
                    properties = []
                properties.append(self.fetch_property(child))
                
            elif child.name == "aspect":
                if aspects is None:
                    aspects = []
                aspects.append(self.fetch_aspect(child))
            
        bean.set_init_arguments(arguments)
        bean.set_properties(properties)
        bean.set_aspects(aspects)
        
        context.xpathFreeContext() 
               
        self.load_definition(id, bean)
        return bean
        
    def fetch_argument(self, node):        
        arg = definitions.ArgumentBeanDefinition()
        
        child = node.children
        while child is not None:
                        
            if child.type == "element":
                arg.set_type("bean")                
                arg.set_value(child.prop("bean"))
                       
            elif child.type == "text":
                arg.set_type("plain")
                arg.set_value(child.content)
            
            child = child.next

        return arg
        
    def fetch_property(self, node):
        property = definitions.PropertyBeanDefinition()
        property.set_name(node.prop("name"))

        child = node.children
        while child is not None:           
            if child.type == "element":                
                property.set_type("bean")            
                property.set_value(child.prop("bean"))                
                
            child = child.next
         
        if property.get_value() is None:
            property.set_type("plain")
            property.set_value(node.content);
        
        return property

    def fetch_aspect(self, node):
        aspect = definitions.AspectBeanDefinition()
        aspect.set_bean(node.prop("ref"))
        
        pointcuts = []
        child = node.children
        while child is not None:
            if child.name == "pointcut":
                pointcuts.append(child.prop("method"))
            
            child = child.next

        if len(pointcuts) is not 0:
            aspect.set_pointcuts(pointcuts)
            return aspect
            
        raise definitions.AspectBeanDefinitionException(
            "aspect pointcuts must be defined"
        )
            
    def has_definition(self, id):
        if id in self.cache or self.in_cache(id):
            return True            
        return False
    
    def in_cache(self, id):
        if self.cacheEnable is False:
            return False
        
        if os.path.isfile(self.cacheDirectory + "/" + id.lower() + ".def"):
            return True
        
        return False
    
    def get_loaded_definition(self, id):
        if id in self.cache:            
            return self.cache[id]
        
        if self.cacheEnable is not False:
            filename = self.cacheDirectory + "/" + id.lower() + ".def"
            file = open(filename, "r")
            
            self.cache[id] = pickle.load(file)
            file.close()
                
        return self.cache[id]

    def load_definition(self, id, definition):
        self.cache[id] = definition
                
        if self.cacheEnable is False:
            return
                       
        filename = self.cacheDirectory + "/" + id.lower() + ".def"        
        file = open(filename, "w")
        pickle.dump(definition, file, -1)
        
        
