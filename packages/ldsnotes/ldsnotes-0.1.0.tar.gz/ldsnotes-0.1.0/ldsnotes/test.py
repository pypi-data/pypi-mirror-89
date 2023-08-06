from note import Notes
from annotations import *
from pprint import pprint
from addict import Dict

json = True
try:
    file  = open(".token", 'r')
    token = file.read()
    file.close()
    n = Notes(token=token)
    n[0]
except:
    print("Refetching token...")
    n = Notes("contagon", "6garrett", headless=False)
    file = open(".token", "w")
    file.write(n.token)
    file.close()

print(n[0].markdown())