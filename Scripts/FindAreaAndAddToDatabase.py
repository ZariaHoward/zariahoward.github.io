from collections import namedtuple
Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')

ra = Rectangle(3., 3., 5., 5.)
rb = Rectangle(1., 1., 4., 3.5)
# intersection here is (3, 3, 4, 3.5), or an area of 1*.5=.5

def area(a, b):  # returns None if rectangles don't intersect
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
    if (dx>=0) and (dy>=0):
        return dx*dy

print area(ra, rb)
#  0.5

def percentarea(a,b): #percent of the smallest rectangle that is in overlap region
    a_area = (a.xmax-a.xmin) * (a.ymax-a.ymin)
    b_area = (b.xmax-b.xmin) * (b.ymax-b.ymin)
    a_and_b_area = area(a,b)
    if a_and_b_area is None:
        
        return 0.0
    else: return a_and_b_area*1.0/min(a_area,b_area)

print percentarea(ra,rb)

#  0.4545454545

from pymongo import MongoClient #version 3.4.0
from bson import ObjectId
from PIL import Image, ImageDraw
import os, sys
import time
client = MongoClient('localhost:27017')
db = client.Teenie

photo_cursor = db.Photos.find({'advancedFaceDetected':{"$exists":"true"}})
count = 0 
for photo in photo_cursor:
    # if count >40: break
    # print photo["path"]
    im = Image.open(photo["path"]).convert('RGBA')
    draw = ImageDraw.Draw(im)
    rectanglesLayer = Image.new('RGBA', im.size, (255,255,255,0)).convert('RGBA')
    d = ImageDraw.Draw(rectanglesLayer)
    rectanglesLayer2 = Image.new('RGBA', im.size, (255,255,255,0)).convert('RGBA')
    d2 = ImageDraw.Draw(rectanglesLayer2)
    rectanglesLayer3 = Image.new('RGBA', im.size, (255,255,255,0)).convert('RGBA')
    d3 = ImageDraw.Draw(rectanglesLayer3)
        
    if "advancedFaceDetected" in photo:
        dlib_faces = photo["advancedFaceDetected"]
        numberOverlap = 0
        if "face_data" in photo:

            for face_id in photo["face_data"]:

                face = db.Faces.find_one({"_id":face_id})
                microsoftR = Rectangle(face["left"],face["top"],face["left"] + face["width"], face["top"]+face["height"])
                d.rectangle([microsoftR.xmin, microsoftR.ymin,microsoftR.xmax, microsoftR.ymax],fill = (255,0,0,80),outline = "red")

                for dlib_face in dlib_faces:
                    dlibR = Rectangle(dlib_face["box"][0] ,dlib_face["box"][1],dlib_face["box"][0]+dlib_face["box"][2],dlib_face["box"][1]+dlib_face["box"][2])
                    d2.rectangle([dlibR.xmin, dlibR.ymin, dlibR.xmax, dlibR.ymax],fill = (0,255,0,80),outline = "green")

                    if percentarea(microsoftR,dlibR) > 0.5:
                        print "Overlapping Faces!" , percentarea(microsoftR,dlibR)
                        db.Faces.update({'_id':face_id}, {"$set": {'d_left':dlib_face["box"][0],'d_top':dlib_face["box"][1],'d_width':dlib_face["box"][2],'faceDetectOverlapPercentage': percentarea(microsoftR,dlibR)}}, upsert=False) #Upsert parameter will insert instead of updating if the post is not found in the database.
                        d3.rectangle( [dlibR.xmin+10, dlibR.ymin+10, dlibR.xmax-10, dlibR.ymax-10] ,fill = (255,255,0,128), outline = "yellow") 

                    elif len(str(percentarea(microsoftR,dlibR))) <= 1:
                        print "Non-Overlapping Faces!" , percentarea(microsoftR,dlibR)
                        print microsoftR
                        print dlibR
                                    
            print numberOverlap                       
            out = Image.alpha_composite(im, rectanglesLayer)
            out = Image.alpha_composite(out, rectanglesLayer2)
            out = Image.alpha_composite(out, rectanglesLayer3)
            out.show()
            time.sleep(4)
            # count += 1


            #There are faces detected by dlib and microsoft "distinguish which ones are which and then add them to the database
            #go through rach face detected by microsoft, if there is a 75% overlap with a dlib, then add those dlib coordinates to that face
            #if not, add a new face to the database with a dlib only tag and the coordinates

            
        else:
            #There are faces detected by dlib but not by microsoft, then add them to the database, and add a "dlib only tag"
            pass
  #           for dlib_face in dlib_faces:
     #           db.Faces.insert({'photoId': photo['_id'],'d_left':dlib_face["box"][0],'d_top':dlib_face["box"][1],'d_width':dlib_face["box"][2]}) #Upsert parameter will insert instead of updating if the post is not found in the database.
'''
    for attrib_key in photo:
        if count >3: break
        
        print(attrib_key)
        continue
        if attrib_key == 'face_data': 

            faces = db.Faces.find({'photoId' : ObjectId(curr_photo['_id'])})
        for obj in faces:
            for part in obj:
                print(part)
                print("woah")
        if (type(curr_photo[attrib_key])== dict) and ("x" in curr_photo[attrib_key]) and ("y" in curr_photo[attrib_key]):
            print(curr_photo[attrib_key]["x"])

'''        
