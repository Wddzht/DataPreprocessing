import numpy as np


def standardization(data_class, handel_index):
    """
    标准化

    -数据无空值
    -数据经过 parse 方法格式转换
    :param data_class:
    :param handel_index:
    :return:
    """
    mean_list = {}
    std_list = {}
    for j in handel_index:
        col = []
        for i in range(len(data_class.data)):
            col.append(data_class.data[i][j])
        mean_list[j] = np.mean(col, axis=0)
        std_list[j] = np.std(col, axis=0)
        col = (col - mean_list[j]) / std_list[j]
        for i in range(len(data_class.data)):
            data_class.data[i][j] = col[i]

    data_class.standard_mean = mean_list
    data_class.standard_std = std_list
    return data_class


def anti_standardization(data_class, handel_index):
    """
    反标准化
    :param data_class:
    :param handel_index:
    :return:
    """
    if not data_class.standard_mean:
        raise ValueError("standard_mean(std) is Null")
    for j in handel_index:
        if j not in data_class.standard_mean:
            raise ValueError(j + " is not in standard_mean(std):" + data_class.standard_mean)

    for i in range(len(data_class.data)):
        for j in handel_index:
            data_class.data[i][j] = (data_class.data[i][j] * data_class.standard_std[j]) + data_class.standard_mean[j]
    return data_class
