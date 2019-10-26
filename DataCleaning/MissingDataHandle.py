import DataClass as dc
import numpy as np


def delete_handle(data_class, handel_index):
    """
    删除空值

    要处理的属性不必是数值的
    :param data_class:
    :param handel_index: 要检查的列下标
    :return:
    """
    new_data = []
    for i in range(len(data_class.data)):
        need_delete = False
        for j in handel_index:
            if not data_class.data[i][j]:
                need_delete = True
        if not need_delete:
            new_data.append(data_class.data[i])
    data_class.data = new_data
    return data_class


def fixed_value_padding_handle(data_class, handel_index, padding_value):
    """
    固定值填充

    要处理的属性不必是数值的,只填充空值
    :param data_class:
    :param handel_index: 要检查的列下标
    :return:
    """
    for i in range(len(data_class.data)):
        for j in handel_index:
            if not data_class.data[i][j]:
                data_class.data[i][j] = padding_value
    return data_class


def mode_interpolation_handle(data_class, handel_index):
    """
    众数填充

    要处理的属性必须是整值的，非整值的数值类型计算众数可能会产生错误
    :param data_class:
    :param handel_index:
    :return:
    """
    return __interpolation_handle(data_class, handel_index, 'mode')


def mean_interpolation_handle(data_class, handel_index):
    """
    均数填充

    要处理的属性必须是数值的，不是数值元素按空值处理
    :param data_class:
    :param handel_index:
    :return:
    """
    return __interpolation_handle(data_class, handel_index, 'mean')


def median_interpolation_handle(data_class, handel_index):
    """
    中数填充

    要处理的属性必须是数值的，不是数值元素按空值处理
    :param data_class:
    :param handel_index:
    :return:
    """
    return __interpolation_handle(data_class, handel_index, 'median')


def __interpolation_handle(data_class, handel_index, type):
    data = data_class.data
    need_alert = [[] for _ in range(len(data_class.type_list))]  # 记录需要差值的位置
    data_list = [[] for _ in range(len(data_class.type_list))]  # 记录去除空值后的列表

    for i in range(len(data)):
        for j in handel_index:
            if not data[i][j]:
                need_alert[j].append(i)
            else:
                try:
                    data_list[j].append(float(data[i][j]))
                except ValueError:
                    need_alert[j].append(i)

    for j in handel_index:
        if len(data_list[j]) == len(data):
            continue  # 没有空值

        if type == 'mode':  # 众数
            counts = np.bincount(data_list[j])
            interpol = np.argmax(counts)
        elif type == 'mean':  # 均数
            interpol = np.mean(data_list[j])
        elif type == 'median':  # 中位数
            interpol = np.median(data_list[j])
        else:
            raise NameError(type)
        for i in need_alert[j]:
            data[i][j] = interpol
    return data_class


def mid_interpolation_handle(data_class, handel_index):
    """
    插值法填充
    :param data_class:
    :param handel_index:
    :return:
    """
    data = data_class.data
    need_alert = [[] for _ in range(len(data_class.type_list))]  # 记录需要差值的位置
    data_list = [[] for _ in range(len(data_class.type_list))]  # 记录去除空值后的列表

    for i in range(len(data)):
        for j in handel_index:
            if not data[i][j]:
                need_alert[j].append(i)
            else:
                try:
                    data_list[j].append(float(data[i][j]))
                except ValueError:
                    need_alert[j].append(i)

    for j in handel_index:
        if len(data_list[j]) == len(data):
            continue  # 没有空值

        index = 0
        while index < len(need_alert[j]):
            count = 1  # 连续的空值
            while index + count < len(need_alert[j]) and need_alert[j][index + count] == need_alert[j][index] + count:
                count += 1
            before = after = 0
            i = need_alert[j][index]
            if i > 0:
                before = data[i - 1][j]
            if i + count - 1 < len(data) - 1:
                after = data[i + count - 1 + 1][j]
            if i == 0:
                before = after
            if i + count - 1 == len(data) - 1:
                after = before

            d = (after - before) / (count + 1)
            for c in range(count):
                data[i + c][j] = before + d * (c + 1)

            index = index + count
    return data_class


if __name__ == "__main__":
    data = dc.DataClass([str] + [float] * 12)
    data.read(r"E:\_Python\DataPreprocessing\sample\fz_micro.txt", False)
    # delete_handle(data)
    data.parse()
    mid_interpolation_handle(data, [i for i in range(1, 13)])
    print(data.data)
