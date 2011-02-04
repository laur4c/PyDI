import pydi

inifile = "application.ini"
env = "production"

myContainer = pydi.Container(inifile, env)

print "* Get bean a"
bean = myContainer.get_bean("ABean")
bean.get_property_a("arg1", "arg2")

print "------------------------------------------------------------------------"

print "* Get bean b"
bean = myContainer.get_bean("AnotherBean");
print bean.get_property()
print bean.get_bean()
