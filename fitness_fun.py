import SimpleITK as sitk
import os
import numpy as np

v3d_path=r"C:\Users\admin\Downloads\Vaa3D_v6.007_Windows_64bit\Vaa3D_v6.007_Windows_64bit\v3d_qt6.exe"
dll_path=r"C:\Users\admin\Downloads\Vaa3D_v6.007_Windows_64bit\Vaa3D_v6.007_Windows_64bit\plugins\neuron_utilities\swc_to_maskimage_sphere_unit\swc_to_maskimage_sphere.dll"
app2_path=r"C:\Users\admin\Downloads\Vaa3D_v6.007_Windows_64bit\Vaa3D_v6.007_Windows_64bit\plugins\neuron_tracing\Vaa3D_Neuron2\vn2.dll"

def swc_to_tiff(swc_file,out_file,sz1,sz2,sz3):
    os.system(v3d_path+" /x "+dll_path+" /f swc_to_maskimage /i "+swc_file+" /o "+out_file+" /p "+str(sz1)+" "+str(sz2)+" "+str(sz3))

def get_app2_result(input,output,bkg_thresh=10,b_256cube=1,b_RadiusFrom2D=1,is_gsdt=0,is_gap=0,length_thresh=5,is_resample=1,is_brightfield=1,is_high_intensity=0):
    try:
        img=sitk.ReadImage(input)
        img_data=sitk.GetArrayFromImage(img)
        os.system(v3d_path + " /x " + app2_path + " /f app2 /i " + input + " /o " + output + " /p NULL 0 " + str(
            bkg_thresh))  # " /p [[0["+str(bkg_thresh)+"["+str(b_256cube)+"["+str(b_RadiusFrom2D)+"["+str(is_gsdt)+"["+str(is_gap)+"["+str(length_thresh)+"["+str(is_resample)+"]["+str(is_brightfield)+"]["+str(is_high_intensity)+"]]]]]]]]]")
    except:
        print(input," is not exist!")
        img_data=np.zeros((1,1,1))
    #os.system(v3d_path+" /x "+app2_path+" /f app2 /i "+input+" /o "+output+" /p NULL 0 "+str(bkg_thresh))#" /p [[0["+str(bkg_thresh)+"["+str(b_256cube)+"["+str(b_RadiusFrom2D)+"["+str(is_gsdt)+"["+str(is_gap)+"["+str(length_thresh)+"["+str(is_resample)+"]["+str(is_brightfield)+"]["+str(is_high_intensity)+"]]]]]]]]]")
    return img_data.shape

def dice(swc_gt,swc_result):
    try:
        gt=sitk.ReadImage(swc_gt)
        gt_data=sitk.GetArrayFromImage(gt)
    except:
        print("rswc tiff is not exist!")
        return -1e-3

    try:
        result=sitk.ReadImage(swc_result)
        result_data=sitk.GetArrayFromImage(result)
    except:
        print("output tiff is not exist!")
        return -1e-3

    gt_data[gt_data!=0]=1
    result_data[result_data!=0]=1
    print(gt_data.shape,result_data.shape)
    if gt_data.shape!=result_data.shape:
        return -1e-3
    inter=np.sum(gt_data*result_data)

    union=np.sum(gt_data)+np.sum(result_data)

    dice=(2.*inter+1)/(union+1)

    return dice

def fitness_func(swc_file,out_file,rswc):
    swc_to_tiff(swc_file,out_file)
    dice(out_file,rswc)

if __name__=="__main__":
    # a=r"D:\A_DLcsz\DLtrain\fixed_data\label\seg_ImgSoma_17302_00020-x_14992.3_y_21970.3_z_4344.8.tiff"
    # b=r"D:\A_DLcsz\DLtrain\fixed_data\label\seg_ImgSoma_17302_00021-x_15598.6_y_22235.2_z_4278.4.tiff"
    # c=r"D:\A_DLcsz\DLtrain\fixed_data\label\seg_ImgSoma_17302_00020-x_14992.3_y_21970.3_z_4344.8.tiff"
    # print(dice(a,b))
    # input=r"C:\Users\admin\Desktop\Converted_Image.tiff"
    # output = r"C:\Users\admin\Desktop\Converted_Image.tiff_app2.swc"
    # get_app2_result(input,output)
    # a=r"E:\neuron_swc\220225_M_027_0_1_16-05_V2MM_0947_gyc.tiff_app2.swc.tiff"
    # b=r"E:\swc_to_tiff\220225_M_027_0_1_16-05_V2MM_0947_gyc.tiff"
    # print(dice(a,b))
    #swc_to_tiff(r"E:\app2_swc\220217_F_060_0_1_01_11_Cgl_0670_yxq.v3draw.tiff_app2.swc",r"E:\app2_swc\220217_F_060_0_1_01_11_Cgl_0670_yxq.v3draw.tiff_app2.swc.tiff",512,512,191)
    print(dice(r"E:\swc_to_tiff\220217_F_060_0_1_01_11_Cgl_0670_yxq.tiff",r"E:\app2_swc\220217_F_060_0_1_01_11_Cgl_0670_yxq.v3draw.tiff_app2.swc.tiff"))