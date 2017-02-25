#Script so far can be run on a sample size of 5000 in 61 seconds. 
#166 pictures have more than one outlier on a face out of 5000
#801 pictures have more than one outlier on a face out of 5000
# when choosing a random consecutive sample I got 180 and 813 respectively in 5000 pictures
file_name = "/Volumes/HueyFreeman/teenie-faces-1600.json" 
library(rjson)
photoDF = data.frame("x" = integer(),"y"=integer(),"size"=integer(),"conf"=integer())
JsonData <- fromJSON(file = file_name)
lineQualities = c()
oneOutlier = 0
moreThanOneOutlier = 0
for(i in length(JsonData)){ #should be the length of teenie-faces
  numFaces =  length(JsonData[[i]][["faces"]])
  if (numFaces > 0){
    tempDF = data.frame("x" = integer(),"y"=integer(),"size"=integer(),"conf"=integer())
    for (j in 1:numFaces){
      data = c("x" = JsonData[[i]][["faces"]][[j]][["box"]][[1]],"y" = JsonData[[i]][["faces"]][[j]][["box"]][[2]],"size" = JsonData[[i]][["faces"]][[j]][["box"]][[3]],"conf" = JsonData[[i]][["faces"]][[j]][["conf"]])
      photoDF <-rbind(photoDF, data)
      if (numFaces > 3){
        tempDF <- rbind(tempDF,data)
      }
    }
    if (numFaces > 3){
      print(i)
      linModel = lm(tempDF[[2]]~tempDF[[1]])
      deviation = sd(resid(linModel))
      lineQualities = c(lineQualities, deviation)
      distanceChecker = pf(cooks.distance(linModel),2,numFaces-2) # f dist from 2 to n-2
      outlierDistances <- distanceChecker[which(distanceChecker > 0.5)] #weights on the F-dist of outliers that stray too far from the line
      if (length(outlierDistances) > 0) {
        oneOutlier = oneOutlier + 1
        if (length(outlierDistances) > 1) {
          moreThanOneOutlier = moreThanOneOutlier + 1
        }
        }
      }
    
    }
}

print(oneOutlier)
print(moreThanOneOutlier)

names(photoDF) <- c("x","y","size","conf")
plot(photoDF[["x"]], photoDF[["y"]],col = "blue", pch = ".",cex = 2, xlab = "X-Position", ylab = "Y-Position", main = "Plot of Teenie Harris Faces")
hist(photoDF[["x"]], col = "cyan", breaks= "FD", main = "Histogram of X-Positions", xlab= "X-Position")
f = hist(photoDF[["size"]], col = "orange", breaks="FD", main = "Histogram of Face Sizes", xlab= "Face Sizes")
hist(photoDF[["conf"]], col = "purple", breaks="FD", main = "Histogram of Confidence", xlab= "confidence")
hist(lineQualities, probability = TRUE, col = "pink")
lines(density(lineQualities), col = "red", lwd = 3) 

trueindices = which(f$counts > 0)
new_counts = f$counts[trueindices]
new_breaks = f$breaks[trueindices]
new_face_hist_data = cbind(new_breaks,new_counts) #gives the counts of each face size that was picked up (within the margin of error of the size of the break)
#What percentage of the photo do faces take up?
ffd = new_face_hist_data
newFacePixels = new_breaks*as.vector(new_breaks)*as.vector(new_counts)
ans = sum(newFacePixels)/sum(numPixels) #where numPixels is defined in GetPhotoSizes.R

#I want the indicies where count is not equal to zero. and then at those indicies i want the break and the count
