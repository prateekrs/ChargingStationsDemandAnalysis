# load packages
x<-c("Formula", "plm", "foreign", "car", "gplots", "apsrtable", "lmtest", "tseries", "stargazer")
lapply(x, require, character.only=T)


regression_file <- '/Users/mattstringer/research/Houston_analysis/data/regression/regression_file.csv'

mydata <- read.csv(regression_file, header=T, sep = ',')

names(mydata)

mydata <- mydata[mydata$tot_num_buildings != -9999, ]

attach(mydata)

Y_ <- cbind(usage)
X_ <- cbind(tot_num_buildings, tot_num_cardealership, tot_num_condos, tot_num_emergencystation, tot_num_industrial, tot_num_medical, tot_num_offices, tot_num_residential, tot_num_shopping)

pdata <- plm.data(mydata, index=c("id_num", "time"))


model_results <- lm(Y_ ~ X_, data=mydata)
summary(model_results)

sink(file='pooling.txt')
model_results <- plm(Y_ ~ X_, data=pdata, model="pooling")
summary(model_results)
sink(NULL)

sink(file='between.txt')
model_results <- plm(Y_ ~ X_, data=pdata, model="between")
summary(model_results)
sink(NULL)

sink(file='within.txt')
model_results <- plm(Y_ ~ X_, data=pdata, model="within")
summary(model_results)
sink(NULL)