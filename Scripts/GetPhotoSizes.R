file_name = "/Volumes/HueyFreeman/teenie-faces-1600.json" 
library(rjson)

JsonData <- fromJSON(file = file_name)
lineQualities = c()
oneOutlier = 0
moreThanOneOutlier = 0
print(length(JsonData))
sizeDF = data.frame("x" = integer(length(JsonData)),
                    "y"=integer(length(JsonData)),
                    "ratio"=double(length(JsonData)))
for(i in 1:length(JsonData)){ #should be the length of teenie-faces
  x = JsonData[[i]][["originalSize"]][[1]]
  y = JsonData[[i]][["originalSize"]][[2]]
  sizeDF[["x"]][i] = x
  sizeDF[["y"]][i] = y
  sizeDF[["ratio"]][i] = (x/y)
  if (i %% 1000 == 0){
    print(i)
  }
}
#What percentage of the photo do faces take up? to do that we use size df to get total amount of pixels across whole dataset
# element wise multiplication
numPixels = sizeDF[["x"]]*as.vector(sizeDF[["y"]])
newSizeDF=cbind(sizeDF, numPixels)


