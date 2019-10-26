import numpy as np


def z_score_detection(data_class, handel_index, z_thr=3.0):
    """
    Z-score 异常值检测

    -数据无空值
    -数据经过 parse 方法格式转换
    :param data_class:
    :param handel_index:
    :param z_thr:
    :return:
    """
    data = np.array(data_class.data)
    outlier = [[] for _ in range(len(data_class.type_list))]  # 记录离异值的位置(按列)
    for j in handel_index:
        col = data[:, j]
        mean = np.mean(col, axis=0)
        std = np.std(col, axis=0)
        col = (col - mean) / std
        for i in range(len(data_class.data)):
            if col[i] > z_thr or col[i] < -z_thr:
                outlier[j].append(i)
    return outlier


def outlier_none_handle(data_class, handel_index, detection="z_score", *args):
    """
    离异值取空
    :param data_class:
    :param handel_index:
    :param detection:
    :param args:
    :return:
    """
    if detection == "z_score":
        outlier = z_score_detection(data_class, handel_index, args[0])
    else:
        raise NameError(detection)

    for j in range(len(data_class.type_list)):
        for i in outlier[j]:
            data_class.data[i][j] = None
    return data_class
