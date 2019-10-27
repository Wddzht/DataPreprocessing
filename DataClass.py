import LogHelper


class DataClass:
    def __init__(self, type_list, init=None):
        if init:
            self.data = init
        else:
            self.data = []
        self.head = ''
        self.type_list = type_list
        self.normalize_max = {}
        self.normalize_min = {}
        self.standard_mean = {}
        self.standard_std = {}

    def read(self, path, has_head, split_tag='\t'):
        file = open(path)
        if has_head:
            self.head = file.readline()
        for line in file:
            items = line.split(split_tag)
            self.data.append(items)
        return self.data

    def parse(self):
        """
        按 type_list 中的数据类型进行格式转换

        type_list 长度必须等于数据的列数
        与 type_list 中的数据类型不匹配的项填为空值
        :return:
        """
        if not self.data:
            raise ValueError()
        for i in range(len(self.data)):
            if len(self.data[i]) != len(self.type_list):
                raise ValueError(self.data[i])
            for j in range(len(self.type_list)):
                try:
                    self.data[i][j] = self.type_list[j](self.data[i][j])
                except ValueError:
                    # raise ValueError('DataClass.prase():cant convert row{:} {:}'.format(i + 1, self.data[i]))
                    LogHelper.log('DataClass.prase():cant convert row{:} {:}', i + 1, self.data[i])
                    self.data[i][j] = None
        return self.data


if __name__ == "__main__":
    data = DataClass([str] + [float] * 12)
    data.read(r"E:\_Python\DataPreprocessing\sample\fz_micro.txt", False)
    # data.parse()
