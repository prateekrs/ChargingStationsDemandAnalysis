require(corrplot)
require(caret)

load("training.RData")
load("testing.RData") 

trainTarget = trainData[,ncol(trainData)]; 
testTarget = testData[,ncol(testData)];

trainData = trainData[,-ncol(trainData)];
testData = testData[,-ncol(testData)];

affCol = nearZeroVar(trainData)
print(colnames(trainData[,affCol]))
 
trainData = trainData[,-affCol]
testData = testData[,-affCol];

correlations = cor(trainData)
#corrplot(correlations,order="hclust",tl.cex=0.5)

corrCol=findCorrelation(correlations, cutoff = .75)

print(colnames(trainData[,corrCol]))
#remove correlated features
trainData = trainData[,-corrCol]
testData = testData[,-corrCol]

trainData = cbind(trainData,as.matrix(trainTarget));
testData = cbind(testData, as.matrix(testTarget));

save(trainData,file="training.RData")
save(testData,file="testing.RData")
