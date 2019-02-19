# -*- coding:utf-8 -*-
import numpy as np 
class Obstacle():
    def __init__(self):
        self.grids=[]
        self.cloud=[]
        self.score=0.
        self.height=-5.
        self.__MetaType={'META_UNKNOWN':0,
                       'META_SMALLMOT':1,
                       'META_BIGMOT':2,
                       'META_NOMOT':3,
                       'META_PEDESTRAIN':4,
                       'MAX_META_TYPE':5}
        self.meta_type_probs=np.empty(self.__MetaType['MAX_META_TYPE'])
        self.meta_type=self.__MetaType['META_UNKNOWN']
