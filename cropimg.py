from properties import Readimg,Readswc,Writeimg,Writeswc
import SimpleITK as sitk
import math
import numpy as np

def crop_img(img):
    print(img.shape)
    img1 = img[0:256, 0:256,:]      #4
    img2 = img[0:256, 256:512,:]    #3
    img3 = img[256:512, 0:256,:]    #2
    img4 = img[256:512, 256:512,:]  #1
    print(img1.shape)
    print(img2.shape)
    print(img3.shape)
    print(img4.shape)
    img_path1=r"C:\Users\admin\Desktop\croped\1.tiff"
    img_path2 = r"C:\Users\admin\Desktop\croped\2.tiff"
    img_path3 = r"C:\Users\admin\Desktop\croped\3.tiff"
    img_path4 = r"C:\Users\admin\Desktop\croped\4.tiff"
    Writeimg(img1,img_path1)
    Writeimg(img2, img_path2)
    Writeimg(img3, img_path3)
    Writeimg(img4, img_path4)

def set_all_swc(swc,n=0,x=0,y=0,z=0,radius=0,xlim=512,ylim=512,zlim=512):##n:0,type:1,x:2,y:3,z:4,radius:5,parent:6
    #print(swc)
    if n!=0:
        swc[:,0]+=n
        swc[:, 6] += n
    if x!=0:
        swc[:,2]+=x
    if y!=0:
        swc[:,3]+=y
    if z!=0:
        swc[:,4]+=z
    if radius!=0:
        swc[:,5]=radius
    return swc

def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)

def joinswc(swc_f,swc_i,x=0,y=0,z=0,threshold=10):
    swc=set_all_swc(swc_i,n=swc_f.shape[0])
    for i in range(swc_f.shape[0]):
        #print("swc_final: ",i)
        if(x!=0 and (swc_f[i][2]<x-threshold or swc_f[i][2]>x+threshold)):
            continue
        elif (y != 0 and (swc_f[i][3] < y - threshold or swc_f[i][3] > y + threshold)):
            continue
        elif (z != 0 and (swc_f[i][4] < z - threshold or swc_f[i][4] > z + threshold)):
            continue
        for j in range(swc.shape[0]):
            #print("swc_init: ", j)
            if (x != 0 and (swc[j][2] < x - threshold or swc[j][2] > x + threshold)):
                continue
            elif (y != 0 and (swc[j][3] < y - threshold or swc[j][3] > y + threshold)):
                continue
            elif (z != 0 and (swc[j][4] < z - threshold or swc[j][4] > z + threshold)):
                continue
            if(distance(swc_f[i][2:5],swc[j][2:5])<0.5):
                swc[j][6]=swc_f[i][0]
    swc_f=np.append(swc_f,swc,axis=0)
    # print(np.where(swc_f[1:,6]==-1))
    # swc_f=np.delete(swc_f,np.where(swc_f[1:,6]==-1),axis=0)
    # print(swc_f.shape)
    return swc_f

if __name__ == "__main__" :
    img_path = r"C:\Users\admin\Desktop\Converted_Image.tif"
    # swc_path=r"C:\Users\admin\Desktop\croped\3.swc"
    # swc_path1 = r"C:\Users\admin\Desktop\croped\4.swc"
    # swc_path2 = r"C:\Users\admin\Desktop\croped\5.swc"
    # swc=Readswc(swc_path)
    # swc1=Readswc(swc_path1)
    # swc_f=joinswc(swc,swc1,x=256)
    # Writeswc(swc_f,swc_path2)
    # # swc=set_all_swc(swc,y=256)
    # # Writeswc(swc,swc_path1)
    img = Readimg(img_path)
    crop_img(img)
