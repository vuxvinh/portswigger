f = open("numfile.txt",'w')


for i in range(0,10000):
    if (i < 10):
        f.writelines('000'+str(i)+'\n')
    elif (i < 100):
        f.writelines('00'+str(i)+'\n')
    elif(i < 1000):
        f.writelines('0'+str(i)+'\n')
    else:
        f.writelines(str(i)+'\n')

f.close()