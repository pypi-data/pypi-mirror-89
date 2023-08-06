'''
Description: 工具
Author: SongJ
Date: 2020-12-28 14:10:28
LastEditTime: 2020-12-29 14:48:48
LastEditors: SongJ
'''
import time

import matplotlib.pyplot as plt
import numba
import numpy as np
from numba import jit, njit
from scipy.spatial.distance import pdist, squareform
from sklearn.neighbors import BallTree, DistanceMetric, KDTree

from DPTree import DPTree, label_these_node, split_cluster


def fn_timer(*args,**kwargs):
    def mid_fn(function):
        def function_timer(*in_args, **kwargs):
            t0 = time.time()
            result = function(*in_args, **kwargs)
            t1 = time.time()
            print (" %s: %s seconds" %
                (args[0], str(t1-t0))
                )
            return result
        return function_timer
    return mid_fn


@fn_timer("计算距离矩阵")
def calcu_distance(data, metric='euclidean'):
    dist_mat = squareform(pdist(data, metric=metric))
    return dist_mat

@fn_timer("计算截断密度")
@njit
def calcu_cutoff_density(dist_mat, eps):
    '''
    计算截断密度
    '''
    local_cutoff_density = np.where(dist_mat < eps, 1, 0).sum(axis=1)
    local_cutoff_density = local_cutoff_density
    return local_cutoff_density


@fn_timer("计算高斯密度")
@njit
def calcu_gaus_density(dist_mat, eps):
    '''
    计算高斯密度
    '''
    rows = dist_mat.shape[0]
    local_gaus_density = np.zeros((rows,),dtype=np.float32)
    for i in range(rows):
        local_gaus_density[i] = np.exp(-1 *((dist_mat[i, :])/(eps))**2).sum()
        pass
    return local_gaus_density


def calc_density(dist_mat,eps,density_metric):
    if(density_metric=='gauss'):
        return calcu_gaus_density(dist_mat,eps)
    else:
        return calcu_cutoff_density(dist_mat,eps)


def calc_repulsive_force(data,density,dist_mat,k_num,leaf_size,fast=False):
    if(fast):
        denser_pos,denser_dist,density_and_k_relation = calc_repulsive_force_fast(data,k_num,density,leaf_size)
        pass
    else:
        denser_pos,denser_dist,density_and_k_relation = calc_repulsive_force_classical(data,density,dist_mat)
    return denser_pos,denser_dist,density_and_k_relation

@fn_timer("计算斥群值_快速")
def calc_repulsive_force_fast(data, k_num, density, leaf_size):
    #* b. 求每个点的k近邻
    # tree = BallTree(data,leaf_size=2000,metric=DistanceMetric.get_metric('mahalanobis',V=np.cov(data.T)))
    tree = KDTree(data, leaf_size=leaf_size)
    dist, ind = tree.query(data, k=k_num)

    #* 统计 密度 与 k 值的相关性：
    density_and_k_relation = np.zeros((ind.shape[0],2),dtype=np.float32)

    #* c. 计算 k近邻点 是否能找到斥群值
    denser_dist = np.full(ind.shape[0], -1,dtype=np.float32)
    denser_pos = np.full(ind.shape[0],-1,dtype=np.int32)
    for i in range(ind.shape[0]):
        denser_list = np.where(density[ind[i]]>density[i])[0]
        if(len(denser_list)>0):
            denser_dist[i] = dist[i][denser_list[0]]
            denser_pos[i] = ind[i][denser_list[0]] #* 这个pos为data中的下标，没有属性为空的点
            density_and_k_relation[i][0] = density[i]
            density_and_k_relation[i][1] = denser_list[0]
            pass

    #* d. 增加 k值，寻找斥群值:0.
    not_found_data = list(np.where(denser_pos==-1)[0])
    #* 对密度进行排序，剔除密度最大的点
    max_density_idx = not_found_data[np.argmax(density[not_found_data])]
    density[max_density_idx] = density[max_density_idx]+1
    not_found_data.pop(np.argmax(density[not_found_data])) 
    num = 1
    cur_k = k_num
    while(len(not_found_data)>0):
        cur_data_id = not_found_data.pop()
        cur_k = cur_k+k_num
        if(cur_k>=data.shape[0]):
            break
        cur_dist, cur_ind= tree.query(data[cur_data_id:cur_data_id+1], k=cur_k)
        cur_dist, cur_ind = cur_dist[0], cur_ind[0]
        denser_list = np.where(density[cur_ind]>density[cur_data_id])
        while(len(denser_list[0])==0):
            cur_k = cur_k + k_num
            # print("cur_k:",cur_k)
            if(cur_k>=data.shape[0]):
                break
            cur_dist, cur_ind= tree.query(data[cur_data_id:cur_data_id+1], k=cur_k)
            cur_dist, cur_ind = cur_dist[0], cur_ind[0]
            denser_list = np.where(density[cur_ind]>density[cur_data_id])
            pass
        if(len(denser_list[0])>0):
            # print(num)
            # num = num+1
            denser_pos[cur_data_id] = cur_ind[denser_list[0][0]]
            denser_dist[cur_data_id] = cur_dist[denser_list[0][0]]
            density_and_k_relation[cur_data_id][0] = density[cur_data_id]
            density_and_k_relation[cur_data_id][1] = denser_list[0][0]
        else:
            print("没找到:",cur_data_id)
        pass
    denser_dist[max_density_idx] = np.max(denser_dist)+1
    denser_pos[max_density_idx] =max_density_idx
    return denser_pos,denser_dist,density_and_k_relation


@fn_timer("计算斥群值_经典")
def calc_repulsive_force_classical(data,density,dist_mat):
    rows = len(data)
    #* 密度从大到小排序
    sorted_density = np.argsort(density)
    #* 初始化，比自己密度大的且最近的距离
    denser_dist = np.zeros((rows,))
    #* 初始化，比自己密度大的且最近的距离对应的节点id
    denser_pos = np.zeros((rows,), dtype=np.int32)
    for index,nodeId in enumerate(sorted_density):
        nodeIdArr_denser = sorted_density[index+1:]
        if nodeIdArr_denser.size != 0:
            #* 计算比当前密度大的点之间距离：
            over_density_sim = dist_mat[nodeId][nodeIdArr_denser]
            #* 获取比自身密度大，且距离最小的节点
            denser_dist[nodeId] = np.min(over_density_sim)
            min_distance_index = np.argwhere(over_density_sim == denser_dist[nodeId])[0][0]
            # 获得整个数据中的索引值
            denser_pos[nodeId] = nodeIdArr_denser[min_distance_index]
        else:
            #* 如果是密度最大的点，距离设置为最大，且其对应的ID设置为本身
            denser_dist[nodeId] = np.max(denser_dist)+1
            denser_pos[nodeId] = nodeId
    return denser_pos,denser_dist,[]


def calc_gamma(density,denser_dist):
    normal_den = density / np.max(density)
    normal_dis = denser_dist / np.max(denser_dist)
    gamma = normal_den * normal_dis
    return gamma


@fn_timer("自动聚类")
def extract_cluster_auto(data,density,eps,dc_eps,denser_dist,denser_pos,gamma,dist_mat):
    '''
        使用 DPTree 进行数据聚类
        dc_eps：density-connectivity 阈值
    '''
    sorted_gamma_index = np.argsort(-gamma)
    tree = DPTree()
    tree.createTree(data,sorted_gamma_index,denser_pos,denser_dist,density,gamma)
    outlier_forest, cluster_forest=split_cluster(tree,density,dist_mat,eps,dc_eps,denser_dist)
    labels,core_points = label_these_node(outlier_forest,cluster_forest,len(data))
    core_points = np.array(list(core_points))
    labels = labels
    return labels, core_points



