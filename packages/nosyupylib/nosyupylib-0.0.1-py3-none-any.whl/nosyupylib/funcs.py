import mmap
import codecs


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
