import sys
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/core")
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/examples/beans")


import container

inifile = "/export/users/laurac/src/pydi/src/main/resources/application.ini"
env = "production"

myContainer = container.Container(inifile, env)

print "get bean A"
bean = myContainer.get_bean("ABean")
print bean
#    bean.a_method("pepe", "pepa")

bean.prefix_a()

#===============================================================================
# print "========================================================================"
# bean.b_method()
#===============================================================================



#===============================================================================
# print "========================================================================"
# print "get bean B"
# bean = myContainer.get_bean("BBean")
# print bean
# a = bean.get_b()
# a.a_method("arg 1", "arg 3")
# a.b_method()
# a.prefix_a()
#===============================================================================





