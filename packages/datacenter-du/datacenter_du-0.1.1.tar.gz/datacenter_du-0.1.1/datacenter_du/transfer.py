"""上传/下载传输
by tacey@XARC on 2020/12/22
"""

import requests
import threading


# TODO: 单核心上行和下行带宽能占用80%+在办公室网络中18MB/s
# TODO: 能够稳定上传下载不小于100GB的文件型数据集
# TODO: 能够稳定上传下载大批量小文件的数据集（参考量级：≥10000个kb级别的小文件）
# TODO: 能够稳定上传下载大小文件混合的数据集（参考量级：1000个kb级别的文件+ 三个≥10GB文件组合）


class Transfer:
    """Transfer manager interface for upload/download file(s)"""

    # States
    INIT = 0
    DOING = 1
    PAUSED = 2
    MERGING = 3
    FINISHED = 4
    STOPPED = 5

    def __init__(self, url, file_name, chunk_count, high_speed=False, headers=None):
        self.url = url
        self.file_name = file_name
        self.chunk_count = chunk_count
        self.high_speed = high_speed
        if headers is None:
            headers = []
        self.headers = {}
        for header in headers:
            key = header.split(':')[0].strip()
            value = header.split(':')[1].strip()
            self.headers[key] = value

        self.total_length = 0
        self.total_downloaded = 0
        self.total_merged = 0
        self.__chunks = []

        self.last_total = 0
        self.speed = 0
        self.readable_speed = readable_bytes(self.speed)

        self.__state = Transfer.INIT
        self.__subs = []

        self.__progress_lock = threading.Lock()

        self.__async = True
        self.thread = threading.Thread(target=self.run)


def readable_bytes(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1000.0:
            return "{:5.1f} {}{}".format(num, unit, suffix)
        num /= 1024.0
    return "{:5.1f} {}{}".format(num, 'Yi', suffix)


class Chunk(object):
    INIT = 0
    DOING = 1
    PAUSED = 2
    FINISHED = 3
    STOPPED = 4

    def __init__(self, downloader, url, file, start_byte=-1, end_byte=-1, number=-1,
                 high_speed=False, headers=None):
        self.url = url
        self.start_byte = int(start_byte)
        self.end_byte = int(end_byte)
        self.file = file
        self.number = number
        self.downloader = downloader
        self.high_speed = high_speed
        if headers is None:
            headers = {}
        self.headers = headers

        self.__state = Chunk.INIT

        self.progress = 0
        self.total_length = 0
        if self.high_speed:
            self.download_iter_size = 1024 * 512  # 0.4 M
        else:
            self.download_iter_size = 1024  # 1K

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.__state = Chunk.STOPPED

    def pause(self):
        if self.__state == Chunk.DOING:
            self.__state = Chunk.PAUSED
        else:
            print("Cannot pause at this stage")

    def resume(self):
        if self.__state == Chunk.PAUSED:
            print(self.__paused_request)
            self.thread = threading.Thread(target=self.run, kwargs={'r': self.__paused_request})
            self.thread.start()
            print("chunk thread started")

    def get_chunk_count(self):
        """获取分块儿个数："""
        r = requests.head(self.url, stream=True, headers=self.headers)
        if r.status_code != 200:
            raise RuntimeError('无法连接URL:{}'.format(self.url))
        try:
            self.total_length = int(r.headers.get('Content-Length'))
            if r.headers.get('Accept-Ranges') != 'bytes':
                raise RuntimeError('URL does not support ranged requests.')
        except:
            self.chunk_count = 0
        return self.chunk_count

    def run(self, r=None):
        pass

    def is_finished(self):
        return self.__state == Chunk.FINISHED


def download_file(file_url, file_name):
    """download into a file"""
    pass


def download_file_obj(file_url, file_obj):
    """download into  a writeable file-like object.
    The file object must be opened in binary mode, not text mode.
    """
    pass


def upload_file(file_url, file_name):
    """ upload from a file

    :return:
    """


def upload_file_obj(file_url, file_obj):
    """Upload from  a readable file-like object.
    The file object must be opened in binary mode, not text mode.
    """
    pass


