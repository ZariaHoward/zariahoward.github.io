library(RMongo)
mg1 <- mongoDbConnect('Teenie')
print(dbShowCollections(mg1))
# query <- dbGetQuery(mg1, 'test', "{'AGE': {'$lt': 10}, 'LIQ': {'$gte': 0.1}, 'IND5A': {'$ne': 1}}")
# data1 <- query[c('AGE', 'LIQ', 'IND5A')]
# summary(data1)