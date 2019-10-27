import numpy as np


def min_max_normalize(data_class, handel_index):
    """
    离差标准化

    -数据无空值
    -数据经过 parse 方法格式转换
    :param data_class:
    :param handel_index:
    :return:
    """
    max_list = {}
    min_list = {}
    for j in handel_index:
        col = []
        for i in range(len(data_class.data)):
            col.append(data_class.data[i][j])
        max_list[j] = max(col)
        min_list[j] = min(col)
    for i in range(len(data_class.data)):
        for j in handel_index:
            data_class.data[i][j] = (data_class.data[i][j] - min_list[j]) / (max_list[j] - min_list[j])

    data_class.normalize_max = max_list
    data_class.normalize_min = min_list
    return data_class


def anti_min_max_normalize(data_class, handel_index):
    for i in range(len(data_class.data)):
        for j in handel_index:
            data_class.data[i][j] = (data_class.data[i][j] * (
                    data_class.normalize_max[j] - data_class.normalize_min[j])) + data_class.normalize_min[j]
    return data_class
