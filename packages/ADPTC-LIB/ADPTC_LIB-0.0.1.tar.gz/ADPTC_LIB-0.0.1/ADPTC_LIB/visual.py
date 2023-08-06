'''
Description: 可视化结果
Author: SongJ
Date: 2020-12-29 14:47:41
LastEditTime: 2020-12-29 14:49:07
LastEditors: SongJ
'''
import matplotlib.pyplot as plt
import numpy as np


#*************************************** 结果展示*******************************************#
# 绘制密度和时间距离图
def showDenDisAndDataSet(den, dis):
    # 密度和时间距离图显示在面板
    plt.figure(num=1, figsize=(15, 9))
    ax1 = plt.subplot(121)
    plt.scatter(x=den, y=dis, c='k', marker='o', s=30)
    for i in range(len(den)):
        plt.text(den[i],dis[i],i,fontdict={'fontsize':16})
    plt.xlabel('Density')
    plt.ylabel('Distance')
    plt.title('Decision Diagram')
    plt.sca(ax1)
    plt.show()


# 确定类别点,计算每点的密度值与最小距离值的乘积，并画出决策图，以供选择将数据共分为几个类别
def show_nodes_for_chosing_mainly_leaders(gamma):
    plt.figure(num=2, figsize=(15, 10))
    # -np.sort(-gamma) 将gamma从大到小排序
    y=-np.sort(-gamma)
    indx = np.argsort(-gamma)
    plt.scatter(x=range(len(gamma)), y=y, c='k', marker='o', s=50)
    for i in range(int(len(y))):
        plt.text(i,y[i],indx[i],fontdict={'fontsize':16},c='#f00')
    plt.xlabel('n',fontsize=20)
    plt.ylabel('γ',fontsize=20)
    # plt.title('递减顺序排列的γ')
    plt.show()


def show_result(labels, data, corePoints=[]):
    # 画最终聚类效果图
    plt.figure(num=3, figsize=(15, 10))
    # 一共有多少类别
    clusterNum = np.unique(labels)
    scatterColors = [
            '#FF0000','#FFA500','#00FF00','#228B22',
            '#0000FF','#FF1493','#EE82EE','#000000',
            '#00FFFF','#F099C0','#0270f0','#96a9f0',
            '#99a9a0','#22a9a0','#a99ff9','#a90ff9'
    ]

    # 绘制分类数据
    for i in clusterNum:
        if(i==-1 or i==-2):
            colorSytle = '#510101'
            subCluster = data[np.where(labels == i)]
            plt.scatter(subCluster[:, 0], subCluster[:, 1], c=colorSytle, s=80, marker='*', alpha=1)
            continue
        # 为i类别选择颜色
        colorSytle = scatterColors[i % len(scatterColors)]
        # 选择该类别的所有Node
        subCluster = data[np.where(labels == i)]
        plt.scatter(subCluster[:, 0], subCluster[:, 1], c=colorSytle, s=25, marker='o', alpha=1,label=i)
    # 绘制每一个类别的聚类中心
    if(len(corePoints)!=0):
        plt.scatter(x=data[corePoints, 0], y=data[corePoints, 1], marker='+', s=300, c='k', alpha=1)
    # plt.title('聚类结果图')
    plt.legend(loc='upper left',fontsize='18')
    plt.tick_params(labelsize=18)
    plt.show()

def show_data(data):
    plt.figure(num=3, figsize=(15, 10))
    plt.scatter(data[:,0],data[:,1],s=300,edgecolor='')
    for i in range(len(data)):
        plt.text(data[i,0],data[i,1],i,fontdict={'fontsize':16})
    plt.show()



# 绘制密度和时间距离图
def showDenDisAndDataSet_label(den, dis,labels,font_show = True):
        # 一共有多少类别
    clusterNum = np.unique(labels)
    scatterColors = [
            '#FF0000', '#FFA500', '#228B22',
            '#0000FF', '#FF1493', '#EE82EE', '#000000', '#FFA500',
                '#006400', '#00FFFF', '#0000FF', '#FFFACD',
    ]
    # 密度和时间距离图显示在面板
    plt.figure(num=1, figsize=(15, 9))
    ax1 = plt.subplot(121)
    # 绘制分类数据
    for i in clusterNum:
        if(i==-1 or i==-2):
            colorSytle = '#510101'
            subCluster_id = np.where(labels == i)[0]
            plt.scatter(den[subCluster_id], dis[subCluster_id], c=colorSytle, s=200, marker='*', alpha=1)
            continue
        # 为i类别选择颜色
        colorSytle = scatterColors[i % len(scatterColors)]
        subCluster_id = np.where(labels == i)[0]
        plt.scatter(x=den[subCluster_id], y=dis[subCluster_id], c=colorSytle, s=200, marker='o', alpha=1)
    # 绘制每一个类别的聚类中心
    # plt.scatter(x=den[corePoints], y=dis[corePoints], marker='+', s=200, c='k', alpha=1)
    if font_show == True:
        for i in range(len(den)):
            plt.text(den[i],dis[i],i,fontdict={'fontsize':16})
    plt.xlabel('Density - ρ',fontdict={'fontsize':22})
    plt.ylabel('Distance - δ',fontdict={'fontsize':22})
    plt.title('Decision Diagram',fontdict={'fontsize':22})
    plt.sca(ax1)
    plt.show()


# 确定类别点,计算每点的密度值与最小距离值的乘积，并画出决策图，以供选择将数据共分为几个类别
def show_nodes_for_chosing_mainly_leaders_label(gamma,labels,font_show = True):
    # 一共有多少类别
    clusterNum = np.unique(labels)
    scatterColors = [
            '#FF0000', '#FFA500', '#228B22',
            '#0000FF', '#FF1493', '#EE82EE', '#000000', '#FFA500',
                '#006400', '#00FFFF', '#0000FF', '#FFFACD',
    ]
    plt.figure(num=2, figsize=(15, 10))
    # -np.sort(-gamma) 将gamma从大到小排序
    y=-np.sort(-gamma)
    indx = np.argsort(-gamma)
    # 绘制分类数据
    for i in clusterNum:
        if(i==-1 or i==-2):
            colorSytle = '#510101'
            subCluster_id = np.where(labels == i)[0]
            ori_indx = [np.where(indx==i)[0][0] for i in subCluster_id]
            plt.scatter(x=ori_indx, y=gamma[subCluster_id], c=colorSytle, s=200, marker='*', alpha=1)
            continue
        # 为i类别选择颜色
        colorSytle = scatterColors[i % len(scatterColors)]
        subCluster_id = np.where(labels == i)[0]
        ori_indx = [np.where(indx==i)[0][0] for i in subCluster_id]
        plt.scatter(x=ori_indx, y=gamma[subCluster_id], c=colorSytle, s=200, marker='o', alpha=1)
    # plt.scatter(x=range(len(gamma)), y=y, c='k', marker='o', s=50)
    if font_show == True:
        for i in range(int(len(y))):
            plt.text(i,y[i],indx[i],fontdict={'fontsize':16},c='#000')
    plt.xlabel('n',fontsize=20)
    plt.ylabel('γ',fontsize=20)
    # plt.title('递减顺序排列的γ')
    plt.show()

def show_data_label(data,labels,font_show = True):
        # 一共有多少类别
    clusterNum = np.unique(labels)
    scatterColors = [
            '#FF0000', '#FFA500', '#228B22',
            '#0000FF', '#FF1493', '#EE82EE', '#000000', '#FFA500',
                '#006400', '#00FFFF', '#0000FF', '#FFFACD',
    ]
    plt.figure(num=3, figsize=(15, 10))
        # 绘制分类数据
    for i in clusterNum:
        if(i==-1 or i==-2):
            colorSytle = '#510101'
            subCluster_id = np.where(labels == i)[0] 
            plt.scatter(x=data[subCluster_id,0], y=data[subCluster_id,1], c=colorSytle, s=200, marker='*', alpha=1)
            continue
        # 为i类别选择颜色
        colorSytle = scatterColors[i % len(scatterColors)]
        subCluster_id = np.where(labels == i)[0] 
        plt.scatter(x=data[subCluster_id,0], y=data[subCluster_id,1], c=colorSytle, s=200, marker='o', alpha=1)
    
    # plt.scatter(data[:,0],data[:,1],s=300,edgecolor='')
    if font_show == True:
        for i in range(len(data)):
            plt.text(data[i,0],data[i,1],i,fontdict={'fontsize':16})
    plt.show()
