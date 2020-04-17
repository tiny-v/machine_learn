import jieba
import jieba.analyse
import os
from nlp.preprocess import common_utils
from nlp import res_basic_path

# 加载停用词
stop_word_path = os.path.join(res_basic_path, "stop_words.txt")
stop_words = common_utils.load_stop_words(stop_word_path)


def cut_to_list(content):
    """
    :param content:
    :return:
    """
    res = []
    word_list = jieba.lcut(content, cut_all=False, HMM = True)
    print(stop_words)
    for word in word_list:
        if word not in stop_words:
            res.append(word)
    return res

# Test
content = "周福福和来福，来到了网易杭研大楼！"
print(cut_to_list(content))
