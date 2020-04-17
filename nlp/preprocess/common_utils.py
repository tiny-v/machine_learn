import os
import sys
import numpy as np
import pandas as pd
from shutil import copyfile


def read_file(path):
    return open(path, "r", encoding="utf-8", errors='ignore')


def load_stop_words(stop_word_path):
    """
    加载停用词
    :param stop_word_path:
    :return:
    """
    stop_words = []
    with read_file(stop_word_path) as f:
        for line in f.readlines():
            if line is not None:
                stop_words.append(str.strip(line))
    return stop_words


def split_csv(data_file, train_file, test_file, ratio):
    """
    将文件分割按ratio分割
    :param data_file: 
    :param train_file: 
    :param test_file: 
    :param ratio: 
    :return: 
    """
    if int(ratio) == 1:
        try:
            copyfile(data_file.name, train_file.name)
            copyfile(data_file.name, test_file.name)
            print("File copy done!")
        except:
            print("Unexpected error: " + str(sys.exc_info()))
    elif 0 < ratio < 1:
        csv_data = pd.read_csv(data_file, sep='\t', header=None, encoding='utf_8_sig')
        columns = csv_data.columns
        groupby_columns = columns[:-1]
        content_column = columns[-1]
        df_groupby_labels = csv_data.groupby(list(groupby_columns))
        print(csv_data.count())
        print(df_groupby_labels[content_column].count())
        np.random.seed(10)
        for name, group in df_groupby_labels:
            df = df_groupby_labels.get_group(name)[content_column]
            shuffle_indices = np.random.permutation(np.arange(len(df)))
            shuffled = np.array(df)[shuffle_indices]

            # Split train/test set
            test_index = -1 * int(ratio * float(len(df)))
            train, test = shuffled[:test_index], shuffled[test_index:]

            if isinstance(name, tuple):
                name = '\t'.join(name)

            for i in train:
                train_file.write(name + '\t' + (i) + '\n')
            for j in test:
                test_file.write(name + '\t' + (j) + '\n')
    else:
        print('Ratio is not valid. ratio = ' + ratio)


def split_source(source_path, ratio):
    """
    分割数据集为训练集和测试集
    :param source_path: 数据集路径
    :param ratio: 训练集和测试集比例
    :return:
    """
    # 首先检查训练集和验证集是否存在，如果不存在，按照ratio把源文件切分成训练集和验证集
    (filepath, temp_file_name) = os.path.split(source_path)
    (filename, extension) = os.path.splitext(temp_file_name)
    train_dir = os.path.join(filepath, filename + '_train' + extension)
    val_dir = os.path.join(filepath, filename + '_val' + extension)

    if (not os.path.exists(train_dir)) or (not os.path.exists(val_dir)):
        infile = open(source_path, 'r', encoding='UTF-8-sig')
        train_file = open(train_dir, 'w+', encoding='UTF-8-sig')
        val_file = open(val_dir, 'w+', encoding='UTF-8-sig')
        split_csv(infile, train_file, val_file, ratio)
        train_file.close()
        val_file.close()
        infile.close()

