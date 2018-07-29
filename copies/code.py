f=open("facebook/0.feat")
features=[]
for line in f:
    line=line.strip()
    line=line.split(" ")
    for i in range(len(line)):
        line[i]=int(line[i])
#     line[78]=0
#     line[79]=0
#     line[128]=0
    features.append(line[1:])
vis={}

def calcvector(pos1,pos2):
    temp=[]
    for i in range(len(features[pos1])):
    	temp.append(features[pos1][i]*features[pos2][i])
        # temp.append(((len(circles[pos1])*features[pos1][i])+(len(circles[pos2])*features[pos2][i]))/(1.0*(len(circles[pos1])+len(circles[pos2]))))
#     print temp
    return temp

def calcdist(v1,v2):
    ans=0
    prvans=0
    for i in range(len(v1)):
        ans+=((v1[i]-v2[i])**2)
        if(prvans<ans):
        	prvans=ans;
        	# print v1[i],v2[i]
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
            if(calcdist(features[i],features[j])<mindist):
                mindist=calcdist(features[i],features[j]);
                combined[0]=i;
                combined[1]=j;
    print "total iterations",count
    return combined
circles=[]
for i in range(len(features)):
    circles.append([i])
    vis[i]=0
num_circles=len(circles)

while num_circles>24:
    temp=max_circles()
    features.append(calcvector(temp[0],temp[1]))
    print features[temp[0]]
    print features[temp[1]]
    vis[temp[0]]=1
    vis[temp[1]]=1
#     print "hhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
    print len(features)
    vis[len(features)-1]=0
    new=circles[temp[0]]
    for i in range(len(circles[temp[1]])):
        new.append(circles[temp[1]][i])
    circles.append(new)
    print new
    num_circles-=1
    print temp,num_circles

pos=0
for i in range(len(circles)):
    if(vis[i]==1):
        continue
    print "circle",pos,":  ",circles[i]
    pos+=1

featnames=[]
f=open("facebook/0.featnames","r")
for line in f:
    line=line.strip("\n")
    featnames.append(line)

pos=0
for i in range(len(circles)):
    if(vis[i]==1):
        continue
    print "circle",pos,":  ",circles[i]
    if(len(circles[i])<=1):
        print "only one node"
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
        if(ans[k]>0.7*maxi):
            count+=1;
    print "Number of common features:",count
    for k in range(len(ans)):
        if(ans[k]>0.7*maxi):
            print featnames[k]
    print "\n\n\n"
    pos+=1