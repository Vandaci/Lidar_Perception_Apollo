# -*- coding: utf-8 -*-
import numpy as np


class FeatureGenerator:
    def __init__(self):
        self.feature_blob = None
        self.__log_table = np.log1p(np.arange(256))

    def Generate(self, vldpc):
        z = vldpc.z
        rows = vldpc.rows
        cols = vldpc.cols
        grids = rows * cols
        intensity = vldpc.intensity
        map_idx = vldpc.maprow * cols + vldpc.mapcol
        uidx, counts = np.unique(map_idx, return_counts=True)
        max_height_data = np.zeros(grids)  # 单元格最大高度数据
        mean_height_data = np.zeros(grids)  # 单元格平均高度数据
        grid_count = np.zeros(grids)  # 单元格点云数量
        top_intensity_data = np.zeros(grids)  # 单元格最大反射强度
        mean_intensity_data = np.zeros(grids)  # 单元格平均反射强度
        none_empty = np.zeros(grids)  # 单元格是否被占用，占用:1，非占用：0
        for idx, count in zip(uidx, counts):
            idx_tmp = idx == map_idx
            max_height_data[idx] = np.max(z[idx_tmp])
            mean_height_data[idx] = np.mean(z[idx_tmp])
            top_intensity_data[idx] = np.max(intensity[idx_tmp]) / 255
            mean_intensity_data[idx] = np.mean(intensity[idx_tmp]) / 255
            grid_count[idx] = self.__LogCount(count.astype(np.int))
        none_empty[grid_count > 0] = 1
        grid_row, grid_col = np.mgrid[range(rows), range(cols)]
        center_x = self.Pix2Pc(grid_row, rows, vldpc.roi[0, 1])
        center_y = self.Pix2Pc(grid_col, cols, vldpc.roi[1, 1])
        direction_data = np.arctan2(center_y, center_x) / (2 * np.pi)  # Normalized
        distance_data = np.hypot(center_x, center_y) / 60 - 0.5
        self.feature_blob = np.concatenate([max_height_data.reshape((1, 1, rows, cols)),
                                            mean_height_data.reshape((1, 1, rows, cols)),
                                            grid_count.reshape((1, 1, rows, cols)),
                                            direction_data.reshape((1, 1, rows, cols)),
                                            top_intensity_data.reshape((1, 1, rows, cols)),
                                            mean_intensity_data.reshape((1, 1, rows, cols)),
                                            distance_data.reshape((1, 1, rows, cols)),
                                            none_empty.reshape((1, 1, rows, cols))], axis=1)
        return self.feature_blob

    def __LogCount(self, count_data):
        if count_data < 256:
            return self.__log_table[count_data]
        return np.log(1 + count_data)

    @staticmethod
    def F2I(x, rows, lrange):
        return np.floor(rows * (lrange - x) / (2 * lrange)).astype(np.int32)

    @staticmethod
    def Pix2Pc(in_pixel, in_size, out_range):
        res = 2.0 * out_range / in_size
        return out_range - (in_pixel + 0.5) * res


if __name__ == '__main__':
    import pointcloud as pc

    tst = pc.PointCloud()
    tst.ReadFromPcdFile('../../data/test.pcd')
    vld_pc = tst.project2map([-60, 60], [-60, 60], [-5, 5], 640, 640)
    fg = FeatureGenerator()
    fg.Generate(vld_pc)
    pass
