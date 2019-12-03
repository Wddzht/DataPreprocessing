"""
基于粗糙集理论的属性选择.

数据必须满足:
1.离散
2.前n-1条属性是条件属性,第n条属性是决策属性
"""

import numpy as np
import DataClass
import sys


def get_attr_values_dicts(data_class):
    """
    获取数据集中所有属性的取值及个数
    :param data_class:
    :return: [{'value1':count1,'value2':count2},{},...,{}]
    """
    dicts = [{} for _ in range(data_class.attr_count)]
    for i in range(data_class.len):
        for j in range(data_class.attr_count):
            if data_class.data[i][j] not in dicts[j]:
                dicts[j][data_class.data[i][j]] = 1
            else:
                dicts[j][data_class.data[i][j]] += 1


def get_core(data_class):
    """
    返回集合的 CORE 属性集.
    using Discernibility Matrix
    :param data_class:
    :return: 属性所在的下标标量.
    """
    core_attrs = []
    for i in range(data_class.len):
        for j in range(i + 1, data_class.len):
            if data_class.data[i][data_class.attr_count - 1] != data_class.data[j][data_class.attr_count - 1]:
                dis_count = 0
                dis_attr = 0
                for attr in range(data_class.attr_count - 1):
                    if data_class.data[i][attr] != data_class.data[j][attr]:
                        dis_count += 1
                        dis_attr = attr
                if dis_count == 1:
                    core_attrs.append(dis_attr)
    return core_attrs


def check_distinct(data_class, handel_index, considered_instence):
    """
    检查在 handel_index 作为属性集下,是否存在不可区分集.
    :param data_class:
    :param handel_index:
    :return: true 表示没有不可区分集. False 表示存在不可区分集.
    """
    loop_instence = list(considered_instence)
    return_considered_instence = list(considered_instence)
    classify_num = 0
    is_reduct = True
    for i in range(data_class.len):
        if not loop_instence[i]:
            continue
        distinct_set = [i]
        is_distinct_set = True
        for j in range(i + 1, data_class.len):
            if not loop_instence[j]:
                continue
            decision_same = data_class.data[i][data_class.attr_count - 1] == data_class.data[j][
                data_class.attr_count - 1]  # 决策属性是否相同
            condition_same = True  # 选择的条件属性是否都相同
            for attr in handel_index:
                if data_class.data[i][attr] != data_class.data[j][attr]:
                    condition_same = False
                    break
            if condition_same:
                loop_instence[j] = False  # 如果 i 和 j 条件属性相同,则 j 不用再进行计算
                if decision_same:
                    distinct_set.append(j)
                else:
                    is_distinct_set = False
                    break

        if is_distinct_set:
            classify_num += 1
            for item in distinct_set:
                return_considered_instence[item] = False
        else:
            is_reduct = False

    if is_reduct:
        return True, classify_num, []
    else:
        return False, classify_num, return_considered_instence


def attribute_select(data_class):
    """
    在没有不可区分子集(reduct)的情况下,返回产生区分集个数最少的属性集
    当产生的区分集个数相同时,选用取值种类数更少的属性
    :param data_class:
    :return:
    """
    considered_instence = np.array([True] * data_class.len, np.bool)
    selected_attr = get_core(data_class)
    attr_values_dicts = get_attr_values_dicts(data_class)
    is_reduct, classify_num, considered_instence = check_distinct(data_class, selected_attr, considered_instence)
    if is_reduct:
        return selected_attr

    while True:
        if len(selected_attr) == data_class.attr_count - 1:
            raise ValueError('数据集无法进行属性选择')

        min_classify_num_reduct = sys.maxsize
        min_classify_num_no_reduct = sys.maxsize
        considered_instence_no_reduct = []
        select_attr_step = -1
        has_reduct = False
        for attr in range(data_class.attr_count - 1):
            if attr in selected_attr:
                continue
            is_reduct, classify_num, _con = check_distinct(data_class, selected_attr + [attr], considered_instence)
            if is_reduct:
                has_reduct = True
                if classify_num < min_classify_num_reduct:
                    min_classify_num_reduct = classify_num
                    select_attr_step = attr
                elif classify_num == min_classify_num_reduct and len(attr_values_dicts[attr]) < len(
                        attr_values_dicts[select_attr_step]):
                    min_classify_num_reduct = classify_num
                    select_attr_step = attr
            else:
                if has_reduct:
                    continue
                else:
                    if classify_num < min_classify_num_no_reduct:
                        min_classify_num_no_reduct = classify_num
                        select_attr_step = attr
                        considered_instence_no_reduct = _con
                    elif classify_num == min_classify_num_no_reduct and len(attr_values_dicts[attr]) < len(
                            attr_values_dicts[select_attr_step]):
                        min_classify_num_no_reduct = classify_num
                        select_attr_step = attr
                        considered_instence_no_reduct = _con

        if has_reduct:
            return selected_attr + [select_attr_step], min_classify_num_reduct
        else:
            selected_attr = selected_attr + [select_attr_step]
            considered_instence = considered_instence_no_reduct


if __name__ == '__main__':
    data = [['1', '0', '2', '1', '1'],
            ['1', '0', '2', '0', '1'],
            ['1', '2', '0', '0', '2'],
            ['1', '2', '2', '1', '0'],
            ['2', '1', '0', '0', '2'],
            ['2', '1', '1', '0', '2'],
            ['2', '1', '2', '1', '1']]
    dc = DataClass.DataClass([str] * 5, data)

    core = get_core(dc)
    assert core == [1]  # CORE(cd)=1 (the second attr)

    considered_instence = np.array([True] * dc.len, np.bool)
    is_reduct, classify_num, considered_instence = check_distinct(dc, core, considered_instence)
    assert (is_reduct, classify_num, considered_instence) == (False, 1, [False] * 2 + [True] * 5)

    selected_attr, max_classify_num = attribute_select(dc)
    assert selected_attr == [1, 3]
