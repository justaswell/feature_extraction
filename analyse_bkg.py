import os
import numpy as np
import torch
from NNmodel import Fit_model
import matplotlib.pyplot as plt
from config import args

np.set_printoptions(suppress=True)



def readp2app2(txt_path):
    with open(txt_path) as rd:
        lines=rd.readlines()
    return lines

def line_to_numpy(lines):
    data=[]
    for line in lines:
        d=line.split(" ")[1:]
        data.append(d)
    data=np.array(data,dtype=float)
    data=np.around(data,3)
    return data

def train(data):
    torch.set_default_tensor_type(torch.DoubleTensor)

    model = Fit_model()


    for e in range(1000):
        np.random.shuffle(data)
        # print('X=',X)
        #print(e)
        X1 = torch.from_numpy(data)
        min_val_loss = 1e10
        if e%250==0:
            args.lr/=10

        for i in range(data.shape[0]):
            val_loss = 0
            count = 0
            if i < int(data.shape[0]*0.85):
                model.train()
                y_pre = model(X1[i, 1:])
                #print(args.lr)
                loss = model.criterion(y_pre, X1[i][0])
                '''if (e % 2 == 0):
                    print(e, loss.data)'''

                # Zero gradients
                model.opt.zero_grad()
                # perform backward pass
                loss.backward()
                # update weights
                model.opt.step()
            else:
                model.eval()
                y_pre = model(X1[i, 1:])

                loss = model.criterion(y_pre, X1[i][0])
                val_loss += loss
                count += 1
        print('val_loss=', val_loss)
        if val_loss < min_val_loss:
            state = {'model_best': model.state_dict()}
            torch.save(state, 'best_model.pth')  #

def predict(data):
    model=Fit_model()

    Y_pre=[]
    for i in range(data.shape[0]):
        model.eval()
        ckpt = torch.load('best_model.pth')
        model.load_state_dict(ckpt['model_best'])
        W=data[i]#.astype(float)
        W=torch.from_numpy(W)
        W=W.to(torch.float32)
        y_pre=model(W)
        Y_pre.append(y_pre)

    Y_pre=np.array(Y_pre)

    #print(Y_pre)
    return Y_pre

def draw(data,lists):
    x=range(data.shape[0])
    for i in range(data.shape[1]):
        label=lists[i]
        plt.plot(x,data[:,i],label=label)
    plt.legend()
    plt.show()

if __name__=="__main__":
    txt = r"E:\neuron_tiff\p2app2.txt"
    lists=['bkg_threshold','median','mean','sd','percentile_99_5','percentile_00_5']
    lines=readp2app2(txt)
    data=line_to_numpy(lines)
    data=data[:,(0,1,2,3,6,7)]
    data_max=np.max(data,axis=0)
    data_min=np.min(data,axis=0)
    data=(data-data_min)/(data_max-data_min)
    # print(data_max)
    # print(data_min)
    # print(data)
    k=input("train or predict? t/p\n")
    if k=="t":
        train(data[25:40])
    elif k=="p":
        pred = data[:, 1:]
        print(predict(pred[:])*(data_max[0]-data_min[0])+data_min[0])
        print(data[:,0]*(data_max[0]-data_min[0])+data_min[0])
    else:
        print("input is invalid, please input the \"t\" or \"p\"")
    # print(data[60:,0])
    #draw(data,lists)