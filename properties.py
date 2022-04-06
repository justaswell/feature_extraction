from matplotlib import pyplot as plt
from skimage import data,exposure
import glob as glob
import SimpleITK as sitk
from scipy import stats
import numpy as np
import os
np.set_printoptions(suppress=True)

def Readimg(img_path):
    img = sitk.ReadImage(img_path)
    img = sitk.GetArrayFromImage(img)
    img=np.rot90(img,1,axes=(0,2))
    #img = np.rot90(img, 1, axes=(0, 1))
    return img

def Readswc(swc_path):
    swc=[]
    with open(swc_path) as swc_file:
        lines=swc_file.readlines()
        for line in lines:
            if line[0]=="#":
                continue
            line=line.split(" ")
            swc.append(line)
    swc=np.array(swc,dtype='float')
    return swc

def Writeimg(img,img_path):
    img=np.rot90(img,1,axes=(0,2))
    img = sitk.GetImageFromArray(img)
    sitk.WriteImage(img, img_path)

def Writeswc(swc,swc_path):
    with open(swc_path,'w') as swc_file:
        swc_file.write("##n,type,x,y,z,radius,parent\n")
        for i in range(swc.shape[0]):
            line=str(int(swc[i][0]))+" "+str(int(swc[i][1]))+" "+str(swc[i][2])+" "+str(swc[i][3])+" "+str(swc[i][4])+" "+str(swc[i][5])+" "+str(int(swc[i][6]))+"\n"
            swc_file.write(line)


def minsuminterval(img):  #寻找加和95%的最小区间
    # print(img)
    arr = img.flatten()
    # arr[arr<50]=0
    # arr=np.delete(arr,np.where(arr==0))
    n, bins, patches = plt.hist(arr, bins=range(255),density=1)
    print(n)
    plt.show()
    n_sum=np.zeros(n.shape[0])
    for i in range(n.shape[0]):
        n_sum[i]=i*n[i]
    nsum=np.sum(n_sum)
    n_sum /= nsum
    l=0
    r=100
    nmin=255
    fl=0
    fr=255
    while l<=255 and r<=255:
        nsum=np.sum(n_sum[l:r])
        if nsum<0.95:
            r+=1
        else:
            t=r-l
            if t<nmin:
                nmin=t
                fl=l
                fr=r
                l+=1
            else:
                l+=1
    return fl,fr

    # #plt.xlim((0, 255))
    # #print(n)
    # #plt.show()


def grey_moment(img):  #灰度矩 均值、方差、偏移量
    mu=np.mean(img)
    delta=np.std(img)
    skew=np.mean(stats.skew(img))
    return mu, delta, skew

def isValid(X,Y,Z,point):
    if point[0]<0 or point[0]>=X:
        return False
    if point[1]<0 or point[1]>=Y:
        return False
    if point[2]<0 or point[2]>=Z:
        return False
    return True

def getNeighbors(X,Y,Z,x,y,z,dist):
    cn1 = (x + dist, y, z-dist)
    cn2 = (x + dist, y-dist, z)
    cn3 = (x + dist, y+dist, z-dist)
    cn4 = (x + dist, y-dist, z-dist)
    cn5 = (x + dist, y+dist, z)
    cn6 = (x + dist, y, z+dist)
    cn7 = (x + dist, y-dist, z+dist)
    cn8 = (x + dist, y+dist, z+dist)
    cn9 = (x + dist, y, z)
    cn10 = (x - dist, y, z - dist)
    cn11 = (x - dist, y - dist, z)
    cn12 = (x - dist, y + dist, z - dist)
    cn13 = (x - dist, y - dist, z - dist)
    cn14 = (x - dist, y + dist, z)
    cn15 = (x - dist, y, z + dist)
    cn16 = (x - dist, y - dist, z + dist)
    cn17 = (x - dist, y + dist, z + dist)
    cn18 = (x - dist, y, z)
    cn19 = (x , y, z - dist)
    cn20 = (x , y - dist, z)
    cn21 = (x , y + dist, z - dist)
    cn22 = (x , y - dist, z - dist)
    cn23 = (x , y + dist, z)
    cn24 = (x , y, z + dist)
    cn25 = (x , y - dist, z + dist)
    cn26 = (x , y + dist, z + dist)
    points=(cn1,cn2,cn3,cn4,cn5,cn6,cn7,cn8,cn9,cn10,cn11,cn12,cn13,cn14,cn15,cn16,cn17,cn18,cn19,cn20,cn21,cn22,cn23,cn24,cn25,cn26)
    Cn=[]
    for point in points:
        if(isValid(X,Y,Z,point)):
            Cn.append(point)
    return Cn

def corrlogram(image,dist):
    XX,YY,ZZ=image.shape
    print(image.shape)
    cgram=np.zeros((256,256),dtype=np.int)
    for x in range(XX):
        print(x)
        for y in range(YY):
            #print(y)
            for z in range(ZZ):
                #print(z)
                color_i=image[x,y,z]
                neighbors_i=getNeighbors(XX,YY,ZZ,x,y,z,dist)
                for j in neighbors_i:
                    j0=j[0]
                    j1=j[1]
                    j2=j[2]
                    color_j=image[j0,j1,j2]
                    cgram[color_i,color_j]=cgram[color_i,color_j]+1
    return cgram

def collect_intensity_properties(img):
    median = np.median(img)
    mean = np.mean(img)
    sd = np.std(img)
    mn = np.min(img)
    mx = np.max(img)
    percentile_99_5 = np.percentile(img, 99.5)
    percentile_00_5 = np.percentile(img, 00.5)
    return median, mean, sd, mn, mx, percentile_99_5, percentile_00_5

def write_in_txt(lists,txt_path):
    with open(txt_path,"w") as f:
        f.write("filename median mean sd mn mx percentile_99_5 percentile_00_5"+'\n')
        for list in lists:
            f.write(list+'\n')

if __name__=="__main__":
    img_path=r"E:\neuron_tiff\*.tiff"
    txt_path="E:/neuron_tiff/properties.txt"
    img_paths=glob.glob(img_path)
    #print(img_paths)
    lists=[]
    for imgpath in img_paths:
        print(imgpath.split("\\")[-1])
        img=Readimg(imgpath)
        median, mean, sd, mn, mx, percentile_99_5, percentile_00_5=collect_intensity_properties(img)
        lists.append(imgpath.split("\\")[-1]+" "+str(median)+" "+str(mean)+" "+str(sd)+" "+str(mn)+" "+str(mx)+" "+str(percentile_99_5)+" "+str(percentile_00_5))
    write_in_txt(lists,txt_path)


