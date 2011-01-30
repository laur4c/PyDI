import sys
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/core")
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/examples/beans")


import container

inifile = "/export/users/laurac/src/pydi/src/main/resources/application.ini"
env = "production"

myContainer = container.Container(inifile, env)
#===============================================================================
# 
# print "get bean B"
# bean = myContainer.get_bean("BBean")
# 
# print bean
# print bean.get_a()
# print bean.get_b()
#===============================================================================

print "get bean A"
bean = myContainer.get_bean("ABean")
print bean
bean.a_method("pepe", "pepa")

