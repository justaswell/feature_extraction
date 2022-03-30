import glob
import shutil
from fitness_fun import swc_to_tiff
import SimpleITK as sitk

dir=r"E:/neuron_swc/"
dir2=r"E:/neuron_tiff/"

files=glob.glob(dir+"*.eswc")

for file in files:
    name=file.split('\\')[-1].split('.')[0]
    print(name)
    img0=sitk.ReadImage(dir2+name+".v3draw.tiff")
    img=sitk.GetArrayFromImage(img0)

    swc_to_tiff(file,"E:/swc_to_tiff/"+name+".tiff",img.shape[2],img.shape[1],img.shape[0])