import glob
import shutil
from fitness_fun import swc_to_tiff
import SimpleITK as sitk


dir=r"E:\app2_swc\*.txt"

def main():
    files=glob.glob(dir)
    #print(files)
    bkg = []
    for file in files:
        name=file.split('\\')[-1].split('.')[0]
        #print(name)
        with open(file) as readfile:
            lines=readfile.readlines()
            bkg_thre=int(lines[1].split(" ")[-1])
            #print(bkg_thre)
            bkg.append([name,str(bkg_thre)])
    #print(bkg)

    txt_f=r"E:\neuron_tiff\properties.txt"
    #properties=[]
    with open(txt_f) as readfile:
        properties=readfile.readlines()[1:]

    for i in range(len(properties)):
        properties[i]=properties[i].split(" ")
        properties[i][0]=properties[i][0].split(".")[0]
    #print(properties)
    for i in range(len(properties)):
        for j in range(len(bkg)):
            if properties[i][0]==bkg[j][0]:
                for k in range(len(properties[i])):
                    if k==0:
                        continue
                    bkg[j].append(properties[i][k])

    print(bkg)
    txt_wi=r"E:\neuron_tiff\p2app2.txt"
    with open(txt_wi,'w') as f:
        for i in range(len(bkg)):
            f.write(bkg[i][0]+" "+bkg[i][1]+" "+bkg[i][2]+" "+bkg[i][3]+" "+bkg[i][4]+" "+bkg[i][5]+" "+bkg[i][6]+" "+bkg[i][7]+" "+bkg[i][8])

if __name__=="__main__":
    main()
# dir=r"E:/neuron_swc/"
# dir2=r"E:/neuron_tiff/"
#
# files=glob.glob(dir+"*.eswc")
#
# for file in files:
#     name=file.split('\\')[-1].split('.')[0]
#     print(name)
#     img0=sitk.ReadImage(dir2+name+".v3draw.tiff")
#     img=sitk.GetArrayFromImage(img0)
#
#     swc_to_tiff(file,"E:/swc_to_tiff/"+name+".tiff",img.shape[2],img.shape[1],img.shape[0])