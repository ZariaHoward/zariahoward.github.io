import cv2
import sys
import numpy
import contextlib # for urllib.urlopen()
import urllib
import os
import json
import simplejson
from decimal import Decimal
from wand.image import Image
import random
# from matplotlib import pyplot as plt
#When you run over 60000 images, take out #print statements and modifications on other sample code to make it work

#Exports Json
#Exports Vectors for each image

#make a neural net that detects african american faces better in this data set. Also check out edge detection in the PENET photos, notice that all his group photos have a certain shape
#why are these diagonals running through your group shots. They lie on peoples shoulders and under their chinss
def main(argv): 
    #print("in main")                        
    if len(sys.argv) < 2 :
        print("Script Requires a folder as the first argument and a json file as a second argument")
        exit() 

    elif not os.path.isdir(sys.argv[1]):
        print("First argument is not a Directory")
        exit()
    # elif not os.path.exists(sys.argv[2]) and sys.argv[2][-5:] == ".json" :
    #     #print("Second argument is not a .json file")
    #     exit()

    else:  
        # jsonName = pathH = os.getcwd()+"/"+sys.argv[2]
        # j = open(jsonName,"r+")
        # data = json.loads(j.read())

        pathH = sys.argv[1]
        # #print(pathH)

        script_data = {}
        script_data["individuals"] = {}
        script_data["numFaces"] = []
        script_data["faceHorizontalPercentile"] = []
        script_data["faceVerticalPercentile"] = []
        script_data["regressionLineSlopes"] = []
        script_data["regressionLineIntercepts"] = []
        script_data["hoffLineRhos"] = []
        script_data['hoffLineThetas'] = []


        for subdir, dirs, files in os.walk(pathH, topdown= False):
            # for name in dirs:
            #     #print(os.path.join(subdir, name))
            for imageFile in files: 
                if not imageFile.endswith((".png",".jpg",".jpeg",".tif",".tiff")): continue
                # Get user supplied values
                #Has a size limit on how much memory it will take up. So the files need to be resized before run through analysis
                imagePath = (os.path.join(subdir, imageFile)) 
                #print("imagePath:" ,imagePath)
                cascPath = "haarcascade_frontalface_default.xml"
                
                # Create the haar cascade
                faceCascade = cv2.CascadeClassifier(cascPath)

                # Read the image
                image = cv2.imread(imagePath)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                script_data["individuals"][imageFile]= {}
                curDataStructure = script_data["individuals"][imageFile]
                #Detect faces in the image
                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1, #if too small it will throw a cv2.error saying something is not greater or is not equal to zero
                    minNeighbors=50,
                    minSize=(5, 5),
                    flags = cv2.CASCADE_SCALE_IMAGE #cv2.CV_HAAR_SCALE_IMAGE
                )
                dst = cv2.imread(imagePath)
                img_h , img_w = image.shape[0], image.shape[1]
                curDataStructure["img_w"]= img_w
                curDataStructure["img_h"]= img_h
                # #print("size:",img_w , img_h)
                gray_eq = cv2.equalizeHist(gray)
                # gray_eq = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(30,30)).apply(gray)
                scaleFactor = img_w/100.0
                gray_small = cv2.resize(gray, (int(img_w//scaleFactor) , int(img_h//scaleFactor)), dst, 0.5, 0.5)
                gray_small_eq = cv2.resize(gray_eq, (int(img_w//scaleFactor) , int(img_h//scaleFactor)), dst, 0.5, 0.5)
                #cv2.imwrite("resizedEqualized_"+imageFile, gray_small_eq) 


                # #print "Found {0} faces!".format(len(faces))

                #Need a function to choose thresholding value
                #Need a function to pick the correct number of hough lines
                #Need a function to eliminate multiples of hough lines

                # Can use for light dark spatial arrangements, maybe figuring out light source or direction
                # th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                #    12             cv2.THRESH_BINARY,11,2)

                #Maybe using the adaptive thresholding before you feed the images in will allow you to fee
                MaxVal = 80
                MinVal = 20
                edges = cv2.Canny(gray_small_eq,MinVal,MaxVal,apertureSize = 3)
                #view
                

                # #print ("the image: ", type(edges))
                # #print ("for example: ", edges[0])
                def countWhite(image):
                    total = 0
                    white = 0
                    for row in edges:
                        for pixel in row:
                            total+= 1
                            if pixel == 255 : white += 1
                    # #print(total, white)
                    return(white*100.00/total)

                while countWhite(edges) > 16: #14/60 was pretty good
                    # #print countWhite(edges)
                    MaxVal += 20
                    MinVal += 5
                    # #print(MaxVal,MinVal)
                    edges = cv2.Canny(gray_small_eq,MinVal,MaxVal,apertureSize = 3)
                res = numpy.hstack((gray_small,cv2.Canny(gray_small,200,550,apertureSize = 3),gray_small_eq,edges)) #stacking images side-by-side
                
                numPixels = 40 # minimum number of pixels in edge pic to constitute a line
                lines= cv2.HoughLines(edges, 1, numpy.pi/180.0, numPixels, numpy.array([]), 0, 0)
                # #print(lines.shape[0])
                # cv2.imwrite("copy_edges_"+imagePath,edges)
                numLines = 20 #number of houghLines desired
                if lines != None:
                    while lines.shape[0] > numLines: #while the number of non border lines is greater than 15
                        numPixels += 3 #number of pixels in edge pic to constitute a line
                        lines= cv2.HoughLines(edges, 1, numpy.pi/180.0, numPixels, numpy.array([]), 0, 0)
                        # #print(lines.shape[0])
                    def yCoordinate(x,rho,theta):
                        #NOTE: In this function theta is taken in radians
                        return (rho/numpy.sin(theta))-(x*numpy.cos(theta)/numpy.sin(theta))
                    def xCoordinate(y,rho,theta):
                        #NOTE: In this function theta is taken in radians
                        return (numpy.sin(theta)*y - rho)/(-numpy.cos(theta))
                    def isBorder(rho,theta):
                        #NOTE: In this function theta is taken in degrees not in radians
                        a = numpy.cos(theta)
                        b = numpy.sin(theta)
                        x0, y0 = a*rho, b*rho
                        oneCoordPointsList = []
                        average = 0 
                        if int(theta)%90 < 10 or int(theta)%90 >80:
                            #Definitely Perpendicular
                            #print("Perpendicular")
                            if int(theta)%180 < 10 or int(theta)%180 >170:
                                #Definitely Vertical
                                #print("Vertical")
                                for j in range(0,int(img_w),1):
                                    if xCoordinate(j,rho,numpy.deg2rad(theta)) > 0 and xCoordinate(j,rho,numpy.deg2rad(theta)) < img_w : 
                                        pt1 = (xCoordinate(j,rho,numpy.deg2rad(theta)),j)
                                        # #print(pt1)
                                        oneCoordPointsList.append(pt1[0])

                                    # #Trying to use polar
                                    # pt1 = ( int(x0+j*(-b)), int(y0+j*(a)) )
                                    # pt2 = ( int(x0-j*(-b)), int(y0-j*(a)) )
                                    # #Adding x Coordinates to the list when the points are within bounds of the photo and averaging them
                                    # if pt1[1] < img_h and pt1[1] > 0 and pt1[0]>0 and pt1[0] < img_w : oneCoordPointsList.append(pt1[0])
                                    # if pt2[1] < img_h and pt2[1] > 0 and pt2[0]>0 and pt2[0] < img_w : oneCoordPointsList.append(pt2[0])
                                #If you have enough (5) points and the average x coordinate is close enough to the edge (within 20 pixels) it is a border
                                #print("length of list greater than 0:" ,len(oneCoordPointsList) > 0)
                                if len(oneCoordPointsList)>0:
                                    if oneCoordPointsList[0] < 75 or oneCoordPointsList[-1] < 75: 
                                        return "Vertical"
                                    elif oneCoordPointsList[0] > img_w-75 or oneCoordPointsList[-1] >img_w-75: 
                                        return "Vertical"
                                    # average = sum(oneCoordPointsList)/float(len(oneCoordPointsList)) 
                                    # #print("Checking average:",average, "/",img_w)
                                    # #print("absolutes: ",abs(average) < 100, abs(average-img_w )<100)
                                    # if abs(average) < 100 or abs(average-img_w) < 100 : return True 
                                    # else:
                                    #     #print("average too far")
                                    #     color = (137,0,136)

                            else:
                                #Definitely Horizontal
                                #print("Horizontal")
                                # return "Horizontal"
                                
                                for j in range(0,int(img_w),10):
                                    if yCoordinate(j,rho,numpy.deg2rad(theta)) > 0 and yCoordinate(j,rho,numpy.deg2rad(theta)) < img_h :
                                        pt1 = (j, yCoordinate(j,rho,numpy.deg2rad(theta)))
                                        # #print (pt1)
                                        oneCoordPointsList.append(pt1[1])
                                # for j in range(0,int(img_w),5):
                                    # #Trying to use polar
                                    # pt1 = ( int(x0+j*(-b)), int(y0+j*(a)) )
                                    # pt2 = ( int(x0-j*(-b)), int(y0-j*(a)) )
                                    # #Adding y Coordinates to the list and averaging them
                                    # if pt1[0] < img_w and pt1[0] > 0 and pt1[1]>0 and pt1[1] < img_h: oneCoordPointsList.append(pt1[1])
                                    # if pt2[0] < img_w and pt2[0] > 0 and pt2[1]>0 and pt2[1] < img_h : 
                                    #     oneCoordPointsList.append(pt2[1])
                                #print("length of list greater than 0:" ,len(oneCoordPointsList) > 0)
                                if len(oneCoordPointsList)>0:
                                    if oneCoordPointsList[0] < 100 or oneCoordPointsList[-1] < 100: 
                                        return "Horizontal"
                                    elif oneCoordPointsList[0] > img_h-100 or oneCoordPointsList[-1] >img_h-100: 
                                        return "Horizontal"
                                    # average = sum(oneCoordPointsList)/float(len(oneCoordPointsList)) 
                                    # #print("Checking average:",average, "/",img_h)

                                    # #print("absolutes: ",abs(average) < 100, abs(average-img_h )<100)
                                    # if abs(average) < 100 or abs(average-img_h) < 100 : return True 
                                    # else:
                                    #     #print("average too far")
                                    #     color = (137,0,136)

                        return False
       
                    a,b,c = lines.shape
                    curDataStructure["numHoughLines"] = a
                    curDataStructure["noBorderHoughLines"]=[]
                    curDataStructure["borderHoughLines"]=[]
                    for i in range(a):
                        # #print(lines[i])
                        rho = (lines[i][0][0] ) #From upper-left
                        theta = lines[i][0][1]
                        a = numpy.cos(theta)
                        b = numpy.sin(theta)
                        x0, y0 = a*rho, b*rho
                        pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
                        pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
                        # #print(imageFile,scaleFactor)
                        # #print(a,b,x0,y0,pt1,pt2)
                        cv2.line(gray_small_eq, pt1, pt2, (255, 0, 0), 1, cv2.LINE_AA) #only drawing in grayscale???
                        # #print("Rho, Theta :", rho , theta)

                        rho = (lines[i][0][0])*scaleFactor 
                        theta = lines[i][0][1]
                        a = numpy.cos(theta)
                        b = numpy.sin(theta)
                        x0, y0 = a*rho, b*rho
                        pt1 = ( int(x0+2000*(-b)), int(y0+2000*(a)) )
                        pt2 = ( int(x0-2000*(-b)), int(y0-2000*(a)) ) 
                        # #print(imageFile,scaleFactor)
                        # #print(a,b,x0,y0,pt1,pt2)
                        color = (255, 0, 0)
                        if isBorder(rho,numpy.rad2deg(theta)) == "Horizontal" : 
                            color = (0,165,255) #More orange than yellow
                            #print(imageFile+"isBorder:", rho, numpy.rad2deg(theta))
                            curDataStructure["borderHoughLines"].append((Decimal(str(rho)),Decimal(str(theta))))

                        elif isBorder(rho,numpy.rad2deg(theta)) == "Vertical" :
                            color = (104,213,248) #More Yellow than orange
                            #print(imageFile+"isBorder:", rho, numpy.rad2deg(theta))
                            curDataStructure["borderHoughLines"].append((Decimal(str(rho)),Decimal(str(theta))))
                        else :   
                            script_data["hoffLineRhos"].append(Decimal(str(rho)))
                            script_data["hoffLineThetas"].append(Decimal(str(theta))) 
                            #print(imageFile+"isNotBorder:", rho, numpy.rad2deg(theta))
                            curDataStructure["noBorderHoughLines"].append((Decimal(str(rho)),Decimal(str(theta))))
                        cv2.line(image, pt1, pt2, color, 1, cv2.LINE_AA) #only drawing in grayscale???
    #

                        # a , b, x0, y0, = a*2,b*2,x0*2,y0*2
                        # if (pt2[0] - pt1[0]) != 0:

                        #     m = (pt2[1] - pt1[1])/(pt2[0] - pt1[0])
                        #     b = (-1)*m*pt1[0]+pt1[1]
                        #     # ox1, oy1 = (0, m*0+b)
                        #     # ox2, oy2 = (img_w/scaleFactor,m*img_w/scaleFactor+b)

                        #     # nx1, ny1 = (0, int(oy1*scaleFactor))
                        #     # nx2, ny2 = (int(ox2*scaleFactor),int(oy2*scaleFactor))

                        #     pt3 = ( int(pt1[0]*scaleFactor), int(pt1[0]*scaleFactor))
                        #     pt4 = ( int(pt2[0]*scaleFactor), int(pt2[0]*scaleFactor))
                        #     cv2.line(image, pt3, pt4, (255, 0, 0), 1, cv2.LINE_AA)
                        # else:
                        #     x = int(pt2[0]*scaleFactor)
                        #     pt3 = (x , 0)
                        #     pt4 = (x , 1000)
                        #     cv2.line(image, pt3, pt4, (255, 0, 0), 1, cv2.LINE_AA)

                    res2 = numpy.hstack((res,edges,gray_small_eq))
                    # cv2.imshow("compare_"+imagePath,res2)
                    # cv2.imwrite('PENET_'+imageFile,res2)

                # Fails if image has no faces
                # Draw a rectangle around the faces
                bestFitX = []
                bestFitY = []
                script_data["numFaces"].append(len(faces))
                curDataStructure["numFaces"]= len(faces)
                curDataStructure["facePositions"] = []
                if (len(faces) > 0):
                    for (x, y, w, h) in faces:
                        bestFitX.append(x+(w/2))
                        bestFitY.append(y+(h/2))
                        script_data["faceVerticalPercentile"].append(Decimal(str((y+(h/2))*1.0/img_h)))
                        script_data["faceHorizontalPercentile"].append(Decimal(str((x+(w/2))*1.0/img_w)))
                        curDataStructure["facePositions"].append((Decimal(str((x+(w/2)))),Decimal(str(y+(h/2))))) 
                        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                        cv2.line(image,(x+(w/2),0),(x+(w/2),2000),(0,0,255),1)
                        cv2.line(image,(0,y+(h/2)),(2000,y+(h/2)),(0,0,255),1)

                # Draw line of best Fit
                # #print(bestFitX)
                # #print(bestFitY)
                if (len(faces)>4) :
                    bestFitResults = numpy.polyfit(bestFitX,bestFitY,1, full = True) #,cov=True)
                    # #print(imageFile)
                    # #print(".")
                    # #print("# of Faces:", len(faces))
                    # #print("Coeeficients:" ,bestFitResults[0])
                    # #print("Residuals:",bestFitResults[1]) #These are most likely your sum of squared errors. When this is small then the line is useful . Less than 5000 is probably a good number
                    # #print("Rank", bestFitResults[2])
                    # #print("Singular Values", bestFitResults[3])
                    # #print("Rcond", bestFitResults[4])
                    # #print(".")
                    # if bestFitResults[1] < 100000*len(faces): #I suspect bestfitresults[1] is the sum of squared errors against the line.
                    bestFitResults = numpy.polyfit(bestFitX,bestFitY,1)
                    def variation(faces, intercept, slope):
                        errorArray=[]
                        for (x, y, w, h) in faces:
                            faceX=x+(w/2)
                            faceY=y+(h/2)
                            lineFaceY= intercept + faceX*slope
                            error = lineFaceY - faceY
                        mean,sd = cv2.meanStdDev(numpy.array(errorArray))
                        mean,sd = mean[0][0],sd[0][0]
                        return (mean,sd)


                    if variation(faces,bestFitResults[1],bestFitResults[0])[1] < 30:
                        # bestFitResults = numpy.polyfit(bestFitX,bestFitY,1)

                        # #print(int(bestFitResults[0]))
                        # #print(int(bestFitResults[1]*1000 + bestFitResults[0]))
                        # #print(bestFitResults[0]) #note this is the a in ax+b
                        # #print(bestFitResults[1]) #note this is the b in ax+b
                        cv2.line(image,(0, int(bestFitResults[1])),(1000,int(bestFitResults[0]*1000 + bestFitResults[1])),(255,255,0),4)
                        curDataStructure["regressionLine"] = (Decimal(str(bestFitResults[0])),Decimal(str(bestFitResults[1])))
                        script_data["regressionLineIntercepts"].append(Decimal(str(bestFitResults[1])))
                        script_data["regressionLineSlopes"].append(Decimal(str(bestFitResults[0])))

                else:
                    curDataStructure["regressionLine"] = None        

                cv2.imwrite('Final_'+imageFile,image)

                imagePathTwo = "copy_" + imagePath 
                # cv2.imwrite(imagePathTwo, image)
                # cv2.imshow(imagePathTwo, image)
                # cv2.waitKey(0)

        newNum = random.randint(1000, 9999)
        print("random number : ", newNum)
        TeenieHarrisExport = open(str(newNum)+"_Export.json", "w")
        TeenieHarrisExport.write(simplejson.dumps(script_data))
        TeenieHarrisExport.close()

if __name__ == "__main__":
    main(sys.argv[1:])
# 1   First off, look at the bottom of the example and notice that you're calling the main function with sys.argv[1:]. Remember, sys.argv[0] is the name of the script that you're running; you don't care about that for command-line processing, so you chop it off and pass the rest of the list.
# 2   This is where all the interesting processing happens. The getopt function of the getopt module takes three parameters: the argument list (which you got from sys.argv[1:]), a string containing all the possible single-character command-line flags that this program accepts, and a list of longer command-line flags that are equivalent to the single-character versions. This is quite confusing at first glance, and is explained in more detail below.
# 3   If anything goes wrong trying to parse these command-line flags, getopt will raise an exception, which you catch. You told getopt all the flags you understand, so this probably means that the end user passed some command-line flag that you don't understand.
# 4   As is standard practice in the UNIX world, when the script is passed flags it doesn't understand, you #print out a summary of proper usage and exit gracefully. Note that I haven't shown the usage function here. You would still need to code that somewhere and have it #print out the appropriate summary; it's not automatic.