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

from pydi.definitions import AspectBeanDefinitionException
from pydi.definitions import AspectBeanDefinition
from pydi.definitions import BeanDefinition
from pydi.definitions import ArgumentBeanDefinition
from pydi.definitions import PropertyBeanDefinition
from pydi.Cache import Cache
from BeanNotFoundException import BeanNotFoundException

import logging
import libxml2

class XMLProvider(object):
            
    xmlfile = None    
    cacheEnable = None
    beanDefs = {}
    beanDefCache = None
    
    def __init__(self, options):
        self.xmlfile = options['xml_file']
        self.cacheEnable = options['cache_enable']
        
        if self.cacheEnable is True:
            self.beanDefCache = Cache(options)
        
    def get_bean_definition(self, id):
        if id in self.beanDefs:
            return self.beanDefs[id]
        
        name = self.get_name_by_id(id)
        if self.beanDefCache and self.beanDefCache.has(name):
            return self.beanDefCache.fetch(name)
        
        return self.get_from_xml(id, self.get_beandef_from_xml)
    
    def get_from_xml(self, id, getBeanDef):
        doc = self.__get_xmldoc()        
        context = doc.xpathNewContext()
        
        try:
            # verify if bean is configured 
            xmlNode = context.xpathEval("//bean[@id='" + id + "']")
            xmlNode = xmlNode[0]
            
        except IndexError as exception:
            raise BeanNotFoundException(id + " bean not found ")
        
        beanDef = getBeanDef(id, xmlNode)
        
        context.xpathFreeContext()
        return beanDef
        
    
    def get_beandef_from_xml(self, id, xmlNode):
        """
        Parse xml configuration and returns the bean definition        
        @param id: ID Attribute of bean node        
        """
        
        #initialize bean definition
        beanDef = BeanDefinition()
        beanDef.set_id(id)
        beanDef.set_fullname(xmlNode.prop("fullname"))
        
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
            
        beanDef.set_init_arguments(arguments)
        beanDef.set_properties(properties)
        beanDef.set_aspects(aspects)                

        self.store(id, beanDef)
        return beanDef
        
    def fetch_argument(self, node):        
        arg = ArgumentBeanDefinition()
        
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
        property = PropertyBeanDefinition()
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
        aspect = AspectBeanDefinition()
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
            
        raise AspectBeanDefinitionException(
            "aspect pointcuts must be defined"
        )
            
    def store(self, id, beanDef):
        self.beanDefs[id] = beanDef
        
        if self.beanDefCache:
            name = self.get_name_by_id(id)
            self.beanDefCache.store(name, beanDef)        

    def get_name_by_id(self, id):
        return id.lower() + ".def"
        
    def __get_xmldoc(self):
        return libxml2.parseFile(self.xmlfile)        
        
        
