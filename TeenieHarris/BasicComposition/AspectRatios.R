rm(list = ls())
m <- mongo(db = "Teenie", collection = "Photos")
m$count()
sample = data.frame(m$find('{"aspect_ratio" : {"$exists": true}}'))
#NOTE: It's doing some thing weird with facedata, where it makes multiples of a photo for each face in face_data

ggplot(data = sample, aes(sample$aspect_ratio), bins = 20)+
  geom_histogram(bins = 40)+xlab("Aspect Ratio")+ylab("Number of Photos")+
  labs(title = "Histogram of Aspect Ratios in Teenie Harris Archive")

plot.new()

#172 - square , 14564 - vertical, 31814 - horizontal
ggplot(data = sample, aes(sample$orientation), bins = 20)+
  geom_bar()+xlab("Aspect Ratio")+ylab("Number of Photos")+
  labs(title = "Orientation of Photos in Teenie Harris Archive")