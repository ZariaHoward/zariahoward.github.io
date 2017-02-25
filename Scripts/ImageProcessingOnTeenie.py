
# coding: utf-8

# In[20]:

from PIL import Image
from PIL import ImageFilter
from PIL import ImageOps
from __future__ import print_function
from pymongo import MongoClient
from bson import ObjectId
client = MongoClient('localhost:27017')
db = client.Teenie


# In[ ]:

im = Image.open("/Users/zariahoward/Desktop/Box_085/13321.png").convert("RGB")
print(im.format, im.size, im.mode)
box = (100, 100, 400, 400) # (x,y,w,h)
region = im.crop(box) # get a portion of the image the size of the box
region = region.transpose(Image.ROTATE_180) 
# out = im.transpose(Image.FLIP_LEFT_RIGHT)
# out = im.transpose(Image.FLIP_TOP_BOTTOM)
# out = im.transpose(Image.ROTATE_90)
# out = im.transpose(Image.ROTATE_180)
# out = im.transpose(Image.ROTATE_270)
im.paste(region, box)
im.show()


# In[4]:

def roll(image, delta):
    "Roll an image sideways"

    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))

    return image


# In[6]:

rolled_im = roll(im,500)  #shifts an image in a special way. Very nice effect
rolled_im.show()


# In[13]:

# split the image into individual bands
source = im.split()
print(len(source))
R, G, B, A = 0, 1, 2, 3

# select regions where red is less than 100
mask = source[R].point(lambda i: i < 100 and 255)

# process the green band
out = source[G].point(lambda i: i * 0.4)

# paste the processed band back, but only where red was < 100
source[G].paste(out, None, mask)

# build a new multiband image
im = Image.merge(im.mode, source) #takes a  mode and a source
im.show()


# In[16]:

120 < 100 and 255


# In[21]:

blurred_image = im.filter(ImageFilter.GaussianBlur(radius = 20))
blurred_image.show()


# In[28]:

inverted_image = ImageOps.invert(blurred_image)
inverted_image.show()


# In[ ]:

http://pillow.readthedocs.io/en/3.0.x/handbook/tutorial.html#color-transforms


# In[39]:


curr_photo = db.Photos.find_one({'path':"/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_082/12966.png" })
for attrib_key in curr_photo:
    print(attrib_key)
    if attrib_key == 'face_data': 

        faces = db.Faces.find({'photoId' : ObjectId(curr_photo['_id'])})
    for obj in faces:
        for part in obj:
            print(part)
            print("woah")
    if (type(curr_photo[attrib_key])== dict) and ("x" in curr_photo[attrib_key]) and ("y" in curr_photo[attrib_key]):
        print(curr_photo[attrib_key]["x"])


# In[14]:

import csv
with open('/Volumes/HueyFreeman/TeenieHarrisGithub/teenie.csv') as csvfile:
    reader = csv.DictReader(csvfile)
#     "web_url": "http://www.cmoa.org/CollectionDetail.aspx?item=445"
    for row in reader:
        if "item=" + str(71757) in row['web_url']:
            print(row['title'])
            break


# In[7]:

filename = "/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_098/1234.png"
filenumber = filename[filename.index("Box")+8:-4]
print("item="+ filenumber)


# In[ ]:



