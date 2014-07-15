setwd("C:\\Users\\Prateek Raj\\Desktop\\EV_ChargingDataAnalysis\\AnalyzingData\\HoustonAnalysis")
data<-read.csv("houston.csv")
str(data)
data_filtered<-data[data$KWH.Used>0.25,]
data_filtered$Transaction.Date<-as.POSIXlt(strptime(data_filtered$Transaction.Date, "%m/%d/%Y %H:%M"))
data_filteredDC<-data_filtered[data_filtered$DC.L2=="DC",]
data_filteredL2<-data_filtered[data_filtered$DC.L2=="L2",]

Assetlevels<-levels(factor(data_filteredDC$Asset.Name))

station<-NULL
q<-NULL
counter=0
tab<-NULL
mon_num<-NULL
for(i in seq_along(Assetlevels)) 
{
assetdb<-data_filtered[data_filtered$Asset.Name==Assetlevels[i],]
date_time<-assetdb$Transaction.Date
year<-date_time$year+1900
month<-date_time$mon
d<-data.frame(month,year)
dtable<-table(d)
p<-melt(dtable)
print (dtable)
counter=0
for(j in seq_along(p$month))
{
print(p$month[j])
if (p$value[j]!=0||counter!=0)
{
counter=counter+1
q<-c(q,p$value[j])
station<-c(station,Assetlevels[i])
mon_num<-c(mon_num,counter)
}
}
}
tab$DC_Charging_Station<-station
tab$Month<-mon_num
tab$Frequency<-q

write.csv(tab,"MonthlyDemand-Each_DC_Charging_Station.csv")