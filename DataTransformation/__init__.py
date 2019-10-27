import DataClass as dc
import DataCleaning.MissingDataHandle as mdh
import DataTransformation.NormalizeHandle as nh
import DataTransformation.StandardizationHandle as sdh

if __name__ == "__main__":
    data = dc.DataClass([str] + [float] * 12)
    data.read(r"E:\_Python\DataPreprocessing\sample\fz_micro.txt", False)
    data.parse()
    mdh.mid_interpolation_handle(data, [i for i in range(1, 13)])
    # nh.min_max_normalize(data, [i for i in range(1, 13)])
    # nh.anti_min_max_normalize(data, [i for i in range(1, 13)])
    # for line in data.data:
    #    print('|'.join(['{:.2f}'.format(line[i]) if i > 0 else line[i] for i in range(len(line))]))

    sdh.standardization(data, [i for i in range(1, 13)])
    for line in data.data:
        print('|'.join(['{:.2f}'.format(line[i]) if i > 0 else line[i] for i in range(len(line))]))
