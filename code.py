import sys
file=sys.argv[1]
f=open("facebook/"+file+".feat")
nodetonum={}
numtonode={}
features=[]
circles=[]
vis={}
xx=0
for line in f:
    line=line.strip()
    line=line.split(" ")
    for i in range(len(line)):
        line[i]=int(line[i])
    numtonode[xx]=line[0]
    print line[0],xx
    nodetonum[line[0]]=xx
    vis[xx]=1
    circles.append([xx])
    xx+=1
    features.append(line[1:])


def calcvector(pos1,pos2):
    temp=[]
    for i in range(len(features[pos1])):
    	# temp.append(features[pos1][i]*features[pos2][i])
        temp.append(((len(circles[pos1])*features[pos1][i])+(len(circles[pos2])*features[pos2][i]))/(1.0*(len(circles[pos1])+len(circles[pos2]))))
#     print temp
    return temp

def calcdist(v1,v2):
    ans=-1
    '''for i in range(len(v1)):
        ans+=abs(v1[i]-v2[i])
        	# print v1[i],v2[i]
    return ans'''
    for i in circles[v1]:
        for j in circles[v2]:
            temp=0
            for k in range(len(features[i])):
                temp+=abs(features[i][k]-features[j][k])
            ans=max(ans,temp)
    # ans=(ans*1.0)/(len(circles[v1])*len(circles[v2]))
    return ans

def max_circles():
    mindist=9999999999;
    combined=[1,2]
    count=0
    for i in range(len(features)):
    	# print i
        for j in range(i+1,len(features)):
            # print i,j
            if(vis[i]==1 or vis[j]==1):
                continue
            count+=1
            # if(calcdist(features[i],features[j])<mindist):
            if(calcdist(i,j)<mindist):
                mindist=calcdist(i,j)
                # print mindist
                combined[0]=i
                combined[1]=j
    # print "total iterations",count
    return combined


print "xxxxxxxxxxx",len(features)
# for i in range(len(features)):
#     circles.append([i])
#     vis[i]=1

fcircles=open("./facebook/"+file+".circles","r")
totalcircles=0
for line in fcircles:
    totalcircles+=1
    line=line.strip()
    line=line.split("\t")
    # print "helllllllo",line
    for i in range(1,len(line)):
        # print line[i],nodetonum[int(line[i])]
        vis[nodetonum[int(line[i])]]=0

num_circles=0

for i in (vis):
    # print i
    num_circles+=1-vis[i]
while num_circles>totalcircles:
    temp=max_circles()
    features.append(calcvector(temp[0],temp[1]))
    # print features[temp[0]]
    # print features[temp[1]]
    vis[temp[0]]=1
    vis[temp[1]]=1
#     print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    # print len(features)
    vis[len(features)-1]=0
    new=circles[temp[0]]
    for i in range(len(circles[temp[1]])):
        new.append(circles[temp[1]][i])
    circles.append(new)
    print new
    num_circles-=1
    print temp,num_circles

pos=0
# new_circles=[]
for i in range(len(circles)):
    # new_circles.append(circles[i])
    if(vis[i]==1):
        continue
    # for j in range(len(circles[i])):
        # new_circles[i][j]=numtonode[circles[i][j]]
    print "circle",pos,":  ",circles[i]
    pos+=1

featnames=[]
f=open("facebook/"+file+".featnames","r")
for line in f:
    line=line.strip("\n")
    featnames.append(line)

f=open("outputs/"+file+".newcircles","w")
pos=0
for i in range(len(circles)):
    if(vis[i]==1):
        continue
    print "circle",pos,":  ",circles[i]
    f.write("circle"+str(pos)+": ")
    for j in circles[i]:
        f.write(str(numtonode[j])+",")
    f.write("\n")
    if(len(circles[i])<=1):
        print "only one node"
    print circles[i][0]
    ans=features[circles[i][0]]
    for j in range(1,len(circles[i])):
#         print features[circles[i][j]]
        for k in range(len(features[circles[i][j]])):
            ans[k]=ans[k]+features[circles[i][j]][k]
    print ans
    count=0
    maxi=0
    for k in range(len(ans)):
        maxi=max(maxi,ans[k])
    print maxi
    for k in range(len(ans)):
        if(ans[k]>0.8*maxi):
            count+=1;
    print "Number of common features:",count
    f.write("Number of common features:"+str(count)+"\n")
    for k in range(len(ans)):
        if(ans[k]>0.7*maxi):
            f.write(str(featnames[k])+"\n")
            print featnames[k]
    print "\n\n\n"
    pos+=1
    f.write("\n")
f.close()
