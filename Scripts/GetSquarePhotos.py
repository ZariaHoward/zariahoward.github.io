import shutil
advanced_face_data = None
with open( "/Volumes/HueyFreeman/teenie-faces-1600.json", 'rb' ) as f:
    advanced_face_data = eval(f.read())

for i in xrange(0, len(advanced_face_data)):
    height = advanced_face_data[i]['originalSize'][0]
    width = advanced_face_data[i]['originalSize'][1]
    ratio = (height*1.0)/(width*1.0)
    if (ratio > 0.975 and ratio < 1.025):
        pass
    elif (ratio > 0.92 and ratio < 1.08):
        box_and_file = advanced_face_data[i]['file'][-23:]
        
        try:
            shutil.copy2("/Volumes/HueyFreeman/Teenie_Harris_PNG1024"+box_and_file,"/Users/studio/Desktop/TheSquareTeenies") 
            print box_and_file
        except(IOError):
            pass
##
##
##for i in xrange(1,10): #do (80, 100)
##    cur_dir = "/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_00" + str(i)
##    for root, dirs, files in os.walk(cur_dir):
##        
##for i in xrange(10,100): #do (80, 100)
##    cur_dir = "/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_0" + str(i)
##    for root, dirs, files in os.walk(cur_dir):
##        
##for i in xrange(100,751): #do (80, 100)
##    cur_dir = "/Volumes/HueyFreeman/Teenie_Harris_PNG1024/Box_" + str(i)
##    for root, dirs, files in os.walk(cur_dir):
