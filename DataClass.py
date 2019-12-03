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
            assert len(items) == self.attr_count
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

    def print(self):
        for line in self.data:
            print('|'.join(['{:.2f}'.format(line[i]) if i > 0 else line[i] for i in range(len(line))]))

    def copy(self):
        dc = DataClass(list(self.type_list), list(self.data))
        dc.head = self.head
        dc.type_list = self.type_list
        dc.normalize_max = self.normalize_max
        dc.normalize_min = self.normalize_min
        dc.standard_mean = self.standard_mean
        dc.standard_std = self.standard_std

    @property
    def len(self):
        return len(self.data)

    @property
    def attr_count(self):
        return len(self.type_list)


if __name__ == "__main__":
    data = DataClass([str] + [float] * 12)
    data.read(r".\sample\fz_micro.txt", False)
    # data.parse()
