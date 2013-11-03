from sensnode.plugins import plugins

pi = plugins(init=True)


a = "OK 2 0 0 70 1 242 0 201 38 0 15 17"
raw = a.split(" ")

w = plugins().loadplugins('weathernode')
print w

