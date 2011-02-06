import pydi

options = {
    'xml_file': 'container.xml',
    'log_conf': 'logging.conf',
    'cache_enable': False,
    'cache_directory': '/tmp/laurac/pydicache'
}

myContainer = pydi.Container(options)

bean = myContainer.get_bean("ABean")
bean.get_property_a("arg1", "arg2")

bean = myContainer.get_bean("AnotherBean");
print bean.get_property()
print bean.get_bean().get_property_b()



