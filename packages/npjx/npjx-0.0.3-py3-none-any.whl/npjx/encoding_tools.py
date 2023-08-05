import pandas as pd
import os
import chardet


def GetEncoding(filename, sample_n=100000):
    """
    获取文件编码

    :param sample_n: 读取的字节数量
    :param filename: 文件
    :return: 编码
    """
    with open(filename, 'rb') as f:
        return chardet.detect(f.read(sample_n))


def EncodingConvertTo(filename, target_encoding=None, sample_n=100000):
    """
    转换文件编码格式

    :param filename:
    :param target_encoding:
    :param sample_n:
    :return:
    """
    origin_encoding = GetEncoding(filename, sample_n)['encoding']
    print(f'origin_encoding: {origin_encoding}')
    # 获取【文件名.后缀】
    ext = os.path.splitext(filename)
    if ext[1] == '.csv':
        if 'gb' in origin_encoding or 'GB' in origin_encoding:
            df = pd.read_csv(filename, engine='python', encoding='GBK')
        else:
            df = pd.read_csv(filename, engine='python', encoding='utf-8')
        df.to_csv('Converted_' + ext[0] + ext[1], encoding=target_encoding)
        print(f'target_encoding: {target_encoding}')
        converted_file_enc = GetEncoding('Converted_' + ext[0] + ext[1])['encoding']
        print('Converted_' + ext[0] + ext[1] + f'_encoding: {converted_file_enc}')
    elif ext[1] == '.xls' or ext[1] == '.xlsx':
        if 'gb' in origin_encoding or 'GB' in origin_encoding:
            df = pd.read_excel(filename, encoding='GBK')
        else:
            df = pd.read_excel(filename, encoding='utf-8')
        df.to_excel('Converted_' + ext[0] + ext[1], encoding=target_encoding)
        print(f'target_encoding: {target_encoding}')
        converted_file_enc = GetEncoding('Converted_' + ext[0] + ext[1])['encoding']
        print('Converted_' + ext[0] + ext[1] + f'_encoding: {converted_file_enc}')
    else:
        print('only support csv, xls, xlsx format')


