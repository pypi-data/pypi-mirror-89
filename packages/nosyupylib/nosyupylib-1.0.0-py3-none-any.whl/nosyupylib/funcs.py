import mmap
import codecs
import argparse


def get_num_lines(file_path):
    """
    Get the number of lines of a file
    Source: https://blog.nelsonliu.me/2016/07/30/progress-bars-for-python-file-reading-with-tqdm/
    :param file_path: path of the file
    :return: the number of lines of a file
    """
    fp = codecs.open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def str2bool(v):
    """
    String to boolean value for argparse
    Source: https://stackoverflow.com/a/43357954
    :param v: arg
    :return: True or False
    """
    """string to boolean"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


