filename='C:\Users\Prateek Raj\Desktop\houston_analysis\houston.txt'
file=open(filename,'r')
fwrite='C:\Users\Prateek Raj\Desktop\houston_analysis\houston_short.json'
f=open(fwrite,'w')
f.write('[\n')
line=file.readline()
count=0
while count<=50000:
    line=file.readline()
    while line != '        "type": "Feature"\n':
        f.write(line)
        line=file.readline()
    f.write(line)
    count=count+1
f.write('}\n]')
f.close()
