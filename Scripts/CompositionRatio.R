# [
#   {
#     "file":"/mnt/image_datasets/Teenie/Teenie_Harris_PNG1024/Box_001/686.png",
#     "originalSize": [1277, 1600],
#     "analysisSize": [2556, 3201],
#     "analysisTime": "Wed Oct 19 19:53:39 2016",
#     "scale":2,
#     "faces":[
#       {"conf":0.957002,"box":[743.5,640.5,47.5]}
#       ]
#   },

file_name = "/Volumes/HueyFreeman/teenie-faces-1600.json"
library(rjson)
sizeDF = data.frame("x" = integer(),"y"=integer(),"ratio"=integer())
JsonData <- fromJSON(file = file_name)
for(i in 1:1000){ #should be the length of teenie-faces.. . 1:length(JsonData)
    data = c("x" = JsonData[[i]][["originalSize"]][[1]], "y" = JsonData[[i]][["originalSize"]][[2]], "ratio"= (JsonData[[i]][["originalSize"]][[1]])/(JsonData[[i]][["originalSize"]][[2]]))
    sizeDF <- rbind(sizeDF, data)
}
plot(sizeDF[["x"]], sizeDF[["y"]],col = "blue", pch = ".",cex = 2, xlab = "X-Position", ylab = "Y-Position", main = "Plot of Teenie Harris Faces")
hist(sizeDF[[3]])