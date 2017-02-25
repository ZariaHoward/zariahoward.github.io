import shutil
from pymongo import MongoClient #version 3.4.0
from bson import ObjectId
from PIL import Image, ImageDraw
import os, sys
import time
import json
client = MongoClient('localhost:27017')
db = client.Teenie
advanced_face_data = None


for i in xrange(8,760): 
    cur_dir = "/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_"+("0"*(3-len(str(i))))+ str(i)
    for root, dirs, files in os.walk(cur_dir):
        for file in files: 
            cur_file = os.path.join(root, file)
            if file.endswith(".png"):
                im = Image.open(cur_file)
                cur_size = im.size
                db_photo = db.Photos.find_one({'path': os.path.join(root, file)})
                if db_photo is not None:
                    ratio = (cur_size[0]*1.0)/cur_size[1]
                    if ratio < 0.9:
                        o = "vertical"
                    elif ratio > 1.1:
                        o = "horizontal"
                    else:
                        o = "square"
                    db.Photos.update({"_id":db_photo["_id"]},{"$set":{"im_width": cur_size[0], "im_height": cur_size[1] , "aspect_ratio": ratio , "orientation": o }})
                else:
                    print(file)
                                                          

