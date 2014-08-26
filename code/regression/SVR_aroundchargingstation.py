"""
from sklearn import svm

X = [[0, 0], [2, 2]]
y = [0.5, 2.5]
clf = svm.SVR()
clf.fit(X, y) 

SVR(C=1.0, cache_size=200, coef0=0.0, degree=3,
epsilon=0.1, gamma=0.0, kernel='rbf', max_iter=-1, probability=False,
random_state=None, shrinking=True, tol=0.001, verbose=False)

clf.predict([[1, 1]])
array([ 1.5])
"""
import sklearn
from sklearn import svm
import csv
import random
f = open("C:/Users/Prateek Raj/Desktop/houston_analysis/data/regression/harris/radiusregression1000.csv","rU")
data = csv.reader(f)
data=[row for row in data]
#rowdata=data.split('\r')
header=data[0]
data=data[1:]
print "\n\n\n\n",data[0][0]
usage=[]
print header
for row in data[:]:
    usage.append(row[2])

for row in data[:]:
    #print row[3]
    #print row[4]
    row.remove(row[21])
    row.remove(row[4])
    row.remove(row[3])
    row.remove(row[2])
    row.remove(row[0])
    
for i in range(len(data)):
    #print i, data[i][1]
    for j in range(len(data[i])):
        #print "i="
        #print data[i][j]
        data[i][j]=int(data[i][j])
#        print 'i=',i
#        print 'j=',j

random_list=[]
for i in range(20):
    random_list.append(random.randint(0,len(data)-1))

test_data=[]
test_values=[]
for i in random_list:
    test_data.append(data.pop(i))    
    test_values.append(int(usage.pop(i)))
    for j in range(len(random_list)):
        if random_list[j]>i:
            random_list[j]=random_list[j]-1


print 'datalen=',len(data)
print 'lenofdata=',len(data[0])
print usage[0]
print data[0]
print 'test_values=',test_values

print random_list

C_list=[]
gamma_list=[]

for i in range(-5,16):
    C_list.append(pow(2,i))

for j in range(-15,4):
    gamma_list.append(pow(2,j))

rmax=0
print "C_list=", C_list
print "gamma list=", gamma_list

clf = svm.SVR(C=32,gamma=0.03125)
clf.fit(data, usage)
print "coeff="
print clf.dual_coef_[0][0]

for i in range(len(header)):
    print header[i],clf.dual_coef_[0][i]
    
print header

pred_values=clf.predict(test_data)
       # print 'pred_values=',pred_values
r2=sklearn.metrics.r2_score(test_values,pred_values)
print clf.score(test_values,pred_values)
print r2
""""
for c in C_list:
    for gm in gamma_list:
        clf = svm.SVR(C=c,gamma=gm)
        clf.fit(data, usage)
        pred_values=clf.predict(test_data)
#        print 'pred_values=',pred_values
        r2=sklearn.metrics.r2_score(test_values,pred_values)
        if rmax<r2 or r2>0.75:
            if rmax<r2:
                rmax=r2
                cmax=c
                gmmax=gm
            print rmax
            print "C=",c
            print "gamma=",gm,'\n'
                    

print 'rmax=',rmax
print "Cmax=",cmax
print "gmmax=",gmmax

for row in data[:]:
    i = row.split(',')
    id_num = i[1]
    print "hi"
    time = i[2]
    usage = i[3]
    lat = i[4]
    lon = i[5]


import csv
with open('C:/Users/Prateek Raj/Desktop/houston_analysis/data/regression/regression_file.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\r', quotechar='|')
    for row in spamreader:
        print row
"""
