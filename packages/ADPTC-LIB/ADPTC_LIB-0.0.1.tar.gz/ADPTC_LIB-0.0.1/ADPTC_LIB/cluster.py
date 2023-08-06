'''
Description:
Author: SongJ
Date: 2020-12-28 10:23:45
LastEditTime: 2020-12-29 15:05:40
LastEditors: SongJ
'''

from sklearn.utils import check_array

import myutil
import time

class ADPTC:

    def __init__(self, X, lon_index=0, lat_index=1, time_index=2, attrs_index=[3]):
      self.X = X
      self.lon_index = lon_index
      self.lat_index = lat_index
      self.time_index = time_index
      self.attr_index = attrs_index
      pass


    def clustering(self,eps=0.5, density_metric='cutoff', dist_metric='euclidean', algorithm='auto', knn_num=20, leaf_size=300, connect_eps=1,fast=False):
        '''
            description: 普通聚类，不考虑属性类型，计算混合距离
            return {*}
            eps：
                混合阈值
            density_metric:
                密度计算方式，默认为截断密度，支持 gauss
            dist_metric：
                距离计算方法，默认为 euclidean，支持['euclidean','braycurtis', 'canberra', 'chebyshev', 'cityblock',
                'correlation', 'cosine', 'dice',  'hamming','jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis', 'matching',
                'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
                'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.]
            algorithm：
                近邻计算方法，计算最近邻点及距离，默认'kd_tree',支持['kd_tree','ball_tree','brute','Annoy','HNSW']
            knn_num:
                近邻个数
            leaf_size:
                近邻计算方法中用到的叶子节点个数，会影响计算和查询速度
            connect_eps:
                密度连通性阈值
            fast:
                是否启用快速聚类，通过最近邻查找算法，优化斥群值查找速度
        '''
        start=time.clock()
        try:
            data = check_array(self.X, accept_sparse='csr')
        except:
            raise ValueError("输入的数据集必须为矩阵")
        dist_mat = myutil.calcu_distance(data,dist_metric)
        density = myutil.calc_density(dist_mat,eps,density_metric)
        denser_pos,denser_dist,density_and_k_relation = myutil.calc_repulsive_force(data,density,dist_mat,knn_num,leaf_size,fast)
        if(-1 in denser_pos):
            raise ValueError('阈值太小啦~,或者尝试使用高斯密度呢：density_metric=gauss')
            pass
        gamma = myutil.calc_gamma(density,denser_dist)
        labels, core_points=myutil.extract_cluster_auto(data,density,eps,connect_eps,denser_dist,denser_pos,gamma,dist_mat)
        self.labels = labels
        self.core_points = core_points
        self.density_and_k_relation = density_and_k_relation
        self.density = density
        end=time.clock()
        self.calc_time = str(end-start)
        return self


    def test_version():
        print("迭代测试")
        pass



    