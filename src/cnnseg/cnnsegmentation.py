# -*- coding:utf-8 -*-

import caffe
import cluster2d as ct
import numpy as np
import featuregenerate as fg
import pointcloud as pc


class CNNSegmention:
    def __init__(self):
        self.vldpc = None  # 有效(ROI)投射点云类
        self.feature_blob = None  # 生成的特征通道数据
        self.cnnseg_Net = None  # cnnseg Net 模型
        self.cluster = None  # 簇类
        self.outblobs = None

    def forward(self, proto_path, caffe_model_path,
                PCD_Path, USE_CAFFE_GPU=False, readformat='bin'):
        # 上面提示函数外部已有相同变量名，做到不同
        if USE_CAFFE_GPU:
            caffe.set_mode_gpu()
            caffe.set_device(0)
        else:
            caffe.set_mode_cpu()
        # step1 : feature_generate
        rawpoint = pc.PointCloud()
        if readformat == 'bin':
            rawpoint.ReadFromBinFile(PCD_Path)
        elif readformat == 'pcd':
            rawpoint.ReadFromPcdFile(PCD_Path)
        else:
            print('未知格式,点云读取失败!\n unknow format，Failure!')
        self.vldpc = rawpoint.project2map([-60, 60], [-60, 60], [-5, 5], 640, 640)
        feature = fg.FeatureGenerator()
        self.feature_blob = feature.Generate(self.vldpc)
        # setp2 : load caffe model and forword
        self.cnnseg_Net = caffe.Net(proto_path, caffe_model_path, caffe.TEST)
        self.cnnseg_Net.blobs['data'].data[...] = self.feature_blob
        self.outblobs = self.cnnseg_Net.forward()

    def segment(self, object_thresh=0.5):
        clst = ct.Cluster2d(self.vldpc)
        clst.Cluster(self.outblobs, object_thresh)
        clst.Filter(self.outblobs)
        clst.Classify(self.outblobs)
        clst.GetObjects()
        self.cluster = clst
        return True

    @staticmethod
    def grid2rowcol(grid, cols):
        grid = np.array(grid)
        r = grid // cols
        c = grid % cols
        return r, c


if __name__ == '__main__':
    proto_Path = '../../model/deploy.prototxt'
    caffe_net_path = '../../model/deploy.caffemodel'
    test_bin_path = '../../data/67.bin'
    test_cnnseg = CNNSegmention()
    test_cnnseg.forward(proto_Path, caffe_net_path,
                        test_bin_path, USE_CAFFE_GPU=False, readformat='bin')
    ok = test_cnnseg.segment()
    if ok:
        print('Congratulations! \nAll the tasks have been completed and will generate obstacle information for you.')
        print('Valid objects index:', test_cnnseg.cluster.valid_objects)
        J = 1
        for i in test_cnnseg.cluster.objects:
            print('%i' % J + ':' + i.type, ' score:%f' % i.score)
            J += 1
    else:
        print('Failed! \n Please Check it')
    pass
