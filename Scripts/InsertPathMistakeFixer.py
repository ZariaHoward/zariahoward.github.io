from __future__ import print_function
import time 
import requests
# import cv2
# import operator
import numpy as np

# Import library to display results
# import matplotlib.pyplot as plt
# get_ipython().magic(u'matplotlib inline')
# Display images within Jupyter

import pickle
from pymongo import MongoClient
import pprint
import json as json_lib
import os
import Queue
import threading

client = MongoClient('localhost:27017')
db = client.Teenie

# broken_objects = list(db.Photos.find("path":"true"))

count=0
with open("/Volumes/HueyFreeman/errorPics.txt","r+") as f:
	for subdir, dirs, files in os.walk('/Volumes/HueyFreeman/Teenie_Harris_PNG1024'):
	    for file in files:
	        #print os.path.join(subdir, file)
	        filepath = subdir + os.sep + file

	        if filepath.endswith(".png"):
	        	# print(db.Photos.find({"path":filepath}))
	        	# print(list(db.Photos.find({"path":filepath})))
	        	if len(list(db.Photos.find({"path":filepath}))) == 0:
	        		f.write(filepath+ "\n")
	        		count += 1
	        	else:
	        		print( len(list(db.Photos.find({"path":filepath}))))
f.close()
print(count)