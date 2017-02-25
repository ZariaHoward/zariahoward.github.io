
from pymongo import MongoClient #version 3.4.0
from bson import ObjectId
from PIL import Image, ImageDraw
import os, sys
import time
import json
client = MongoClient('localhost:27017')
db = client.Teenie

data = None
with open('/Users/studio/Desktop/teenie.json') as json_data:
    data = json.load(json_data)

data = data["things"]
for i in xrange(len(data)):
	index = data[i]["web_url"].find("item=")

	if (index == -1): print data[i]["web_url"][index:] 
	else:
		photo_name= data[i]["web_url"][index+5:]
		#db.Photos.find({'path':{"$regex": ".*"+photo_name+".*"}}) --> correct syntax but not what we want
		db_photo = db.Photos.find_one({'path':{"$regex": ".*"+"/"+photo_name+".png"}})
		data[i].pop("creator")
		data[i].pop("images")
		if db_photo is None: 
			print photo_name+".png"
		else:
			db.Photos.update({"_id":db_photo["_id"]},{"$set":data[i]})

	if (i % 1000 == 0 ): print i
			

