#vaa3d -x plugin_name -f app2 -i <inimg_file> -o <outswc_file> -p
#[<inmarker_file> [<channel> [<bkg_thresh> [<b_256cube> [<b_RadiusFrom2D> [<is_gsdt> [<is_gap> [<length_thresh> [is_resample][is_brightfield][is_high_intensity]]]]]]]]]
#channel (0,3) default 0                2
#bkg_thresh (10,138)                    7       [1,3,5,7,9,11,13]
#b_256cube (0,1) default 1              1       [2]
#b_RadiusFrom2D (0,1) default 1         1       [6]
#is_gsdt (0,1) default 0                1       [12]
#is_gap (0,1) default 0                 1       [14]
#length_thresh default 5                3       [4,10,16]
#is_resample (0,1) default 1            1       [15]
#is_brightfield (0,1) default 0         1       [8]
#is_high_intensity (0,1) default 0      1       [0]
#DNA_SIZE=17


import numpy as np
from fitness_fun import get_app2_result,dice,swc_to_tiff
import glob

DNA_SIZE = 7
POP_SIZE = 10
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.005
N_GENERATIONS = 10



def F(bkg_thresh,input,output,rswc):
    pred=[]
    error=False
    for i in range(bkg_thresh.shape[0]):
        img_shape=get_app2_result(input,output,bkg_thresh=bkg_thresh[i])
        swc_to_tiff(output,output+'.tiff',img_shape[2],img_shape[1],img_shape[0])
        print(dice(output+'.tiff',rswc))
        if dice(output+'.tiff',rswc) == -0.001:
            error=True
        pred.append(dice(output+'.tiff',rswc))
    pred=np.array(pred,dtype='float')
    print(pred)
    return pred,error


def get_fitness(pop,input,output,rswc):
    bkg_thresh_ga= translateDNA(pop)
    pred,error = F(bkg_thresh_ga,input,output,rswc)
    return (pred - np.min(pred)) + 1e-3, error # 减去最小的适应度是为了防止适应度出现负数，通过这一步fitness的范围为[0, np.max(pred)-np.min(pred)],最后在加上一个很小的数防止出现为0的适应度


def translateDNA(pop):  # pop表示种群矩阵，一行表示一个二进制编码表示的DNA，矩阵的行数为种群数目
    # channel=pop[:,(8,18)]
    # channel=channel[:,0]*2+channel[:,1]
    bkg_thresh_d=pop[:,:]#(1,3,5,7,9,11,13)]
    bkg_thresh=10
    for i in range(7):
        bkg_thresh+=bkg_thresh_d[:,i]*(2**i)
    # b_256cube = pop[:, 2]
    # b_RadiusFrom2D = pop[:, 6]
    # is_gsdt = pop[:, 12]
    # is_gap = pop[:, 14]
    # length_thresh = pop[:, (4,10,16)]
    # length_thresh=length_thresh[:,0]*4+length_thresh[:,1]*2+length_thresh[:,2]*1+5
    # is_resample = pop[:, 15]
    # is_brightfield = pop[:, 8]
    # is_high_intensity = pop[:, 0]
    return bkg_thresh#,b_256cube,b_RadiusFrom2D,is_gsdt,is_gap,length_thresh,is_resample,is_brightfield,is_high_intensity


def crossover_and_mutation(pop, CROSSOVER_RATE=0.8):
    new_pop = []
    for father in pop:  # 遍历种群中的每一个个体，将该个体作为父亲
        child = father  # 孩子先得到父亲的全部基因（这里我把一串二进制串的那些0，1称为基因）
        if np.random.rand() < CROSSOVER_RATE:  # 产生子代时不是必然发生交叉，而是以一定的概率发生交叉
            mother = pop[np.random.randint(POP_SIZE)]  # 再种群中选择另一个个体，并将该个体作为母亲
            cross_points = np.random.randint(low=0, high=DNA_SIZE )  # 随机产生交叉的点
            child[cross_points:] = mother[cross_points:]  # 孩子得到位于交叉点后的母亲的基因
        mutation(child)  # 每个后代有一定的机率发生变异
        new_pop.append(child)

    return new_pop


def mutation(child, MUTATION_RATE=0.003):
    if np.random.rand() < MUTATION_RATE:  # 以MUTATION_RATE的概率进行变异
        mutate_point = np.random.randint(0, DNA_SIZE )  # 随机产生一个实数，代表要变异基因的位置
        child[mutate_point] = child[mutate_point] ^ 1  # 将变异点的二进制为反转


def select(pop, fitness):  # nature selection wrt pop's fitness
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=(fitness) / (fitness.sum()))
    return pop[idx]


def print_info(pop,txt_path):
    fitness,error = get_fitness(pop,input,output,rswc)
    max_fitness_index = np.argmax(fitness)
    print("max_fitness:", fitness[max_fitness_index])
    x= translateDNA(pop)
    print("最优的基因型：", pop[max_fitness_index])
    print("(x):", (x[max_fitness_index]))
    lines=[]
    lines.append("最优的基因型：  " + str(pop[max_fitness_index]) )
    lines.append("(x):         " + str(x[max_fitness_index]) )
    with open(txt_path,"w") as f:
        for line in lines:
            f.write(line+'\n')


if __name__ == "__main__":

    # input = r"E:\neuron_tiff\220217_F_060_0_1_01_05_RSGb_1298_gyc.v3draw.tiff"
    # output = r"E:\app2_swc\220217_F_060_0_1_01_05_RSGb_1298_gyc.v3draw.tiff_app2.swc"
    # rswc = r"E:\swc_to_tiff\220217_F_060_0_1_01_05_RSGb_1298_gyc.tiff"
    input_path=r"E:\neuron_tiff"
    output_path=r"E:\app2_swc"
    rswc_path=r"E:\swc_to_tiff"

    inputs=glob.glob(input_path+'\*.tiff')
    print(inputs)
    for input in inputs:
        name=input.split('\\')[-1].split('.')[0]
        output=output_path+'\\'+name+".v3draw.tiff_app2.swc"
        rswc=rswc_path+'\\'+name+".tiff"
        # print(input)
        # print(output)
        # print(rswc)
        aerror=False
        pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))  # matrix (POP_SIZE, DNA_SIZE)
        #print(translateDNA(pop).shape)
        for _ in range(N_GENERATIONS):  # 迭代N代
            #x, y = translateDNA(pop)
            pop = np.array(crossover_and_mutation(pop, CROSSOVER_RATE))
            # F_values = F(translateDNA(pop)[0], translateDNA(pop)[1])#x, y --> Z matrix
            fitness,error= get_fitness(pop,input,output,rswc)
            if error is True:
                aerror=True
                break
            pop = select(pop, fitness)  # 选择生成新的种群
        if aerror is True:
            continue
        print_info(pop,output_path+'\\'+name+".txt")
