import sys
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/core")
sys.path.append("/export/users/laurac/src/pydi/src/main/python/ar/com/lec/pydi/examples/beans")


import container

inifile = "/export/users/laurac/src/pydi/src/main/resources/application.ini"
env = "production"

myContainer = container.Container(inifile, env)
#myContainer.load()

aBean = myContainer.get_bean("BBean")
print aBean.get_a()
print aBean.get_b()
asdasdadas



