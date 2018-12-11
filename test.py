import json

#prettify the json
file = open("test_GivingBadNewspt1.json",'w')
json.dump(json.load(open("GivingBadNewspt1.mp3-session.json")), file, indent = 4)
file.close()