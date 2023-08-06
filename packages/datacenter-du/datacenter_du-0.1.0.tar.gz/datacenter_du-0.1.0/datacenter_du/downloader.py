"""下载器
by tacey@XARC on 2020/12/22
"""

import os
import time
import logging
import tempfile
import shutil
import subprocess
import requests
from urllib.parse import urlparse
from requests import Session
import threading
from .transfer import Chunk, readable_bytes


class DownlaoderBase:

    def __init__(self, url, file_name=None, **kwargs):
        self.url = url
        self.file_name = file_name
        if file_name is None:
            self.file_name = urlparse(self.url).path.split("/")[-1]
        else:
            self.file_name = file_name

    def run(self):
        raise NotImplemented


class DownloadChunk(Chunk):

    def run(self, r=None):
        self.__state = Chunk.DOING
        if r is None:
            if self.start_byte == -1 and self.end_byte == -1:
                r = requests.get(self.url, stream=True, headers=self.headers)
            else:
                self.headers['Range'] = "bytes={}-{}".format(str(self.start_byte),
                                                             str(self.end_byte))
                if 'range' in self.headers:
                    del self.headers['range']
                r = requests.get(self.url, stream=True, headers=self.headers)
                self.total_length = int(r.headers.get("content-length"))

        break_flag = False
        for part in r.iter_content(chunk_size=self.download_iter_size):
            self.progress += len(part)
            if part and self.__state != Chunk.STOPPED:
                self.file.write(part)
                if self.__state == Chunk.PAUSED:
                    self.__paused_request = r
                    break_flag = True
                    break
            elif self.__state == Chunk.STOPPED:
                break_flag = True
                break

        if not break_flag:
            self.__state = Chunk.FINISHED


class SimpleDownloader(DownlaoderBase):
    """简单下载器"""

    def __init__(self, url, file_name, **kwargs):
        """构建简单下载器

        :param url: 文件URL
        :param file_name: 目标存储地址
        """
        super().__init__(url, file_name, **kwargs)
        self.url = url
        self.file_name = file_name
        self.headers = kwargs.get("headers", {})
        self.stream = bool(kwargs.get("stream", True))

    def run(self):
        with Session() as session:
            with open(self.file_name, "wb") as f_out:
                resp = session.get(self.url, headers=self.headers, stream=self.stream)
                f_out.write(resp.content)


def simple_download(url, file_name=None, headers=None, stream=True):
    """简单下载(仅支持GET请求)

    requests.get的简单封装

    :param url: 目标
    :param file_name:
    :param headers:
    :param stream:
    """
    with Session() as session:
        with open(file_name, "wb") as f_out:
            resp = session.get(url, headers=headers, stream=stream)
            f_out.write(resp.content)


class Downloader(DownlaoderBase):

    def __init__(self, url, file_name=None, chunk_count=5, **kwargs):
        super().__init__(url, file_name, **kwargs)
        self.chunk_count = chunk_count

    def run(self):
        aria2c = os.getenv("ARIA2C_PATH")
        aria2c = aria2c if aria2c else shutil.which("aria2c")
        if not aria2c:
            logging.warning("使用Python-Downloader")
            return Downloader(url=self.url, file_name=self.file_name,
                              chunk_count=self.chunk_count).run()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        result = subprocess.run(
            [shutil.which("sh"), "-c", '{} "{}" -o "{}" '.format(aria2c, self.url, self.file_name)],
            stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.exception(result.stderr)
        return not (bool(result.returncode))


def download(url, file_name=None, chunk_count=8):
    """下载文件

    :param url:
    :param file_name:
    :param chunk_count:
    """
    Downloader(url=url, file_name=file_name, chunk_count=chunk_count).run()


# split big-file -> multi-part -> every-part chunks

class _Downloader(DownlaoderBase):
    # 文件下载状态
    INIT = 0
    DOWNLOADING = 1
    PAUSED = 2
    MERGING = 3
    FINISHED = 4
    STOPPED = 5

    def __init__(self, url, file_name=None, chunk_count=5, **kwargs):
        super().__init__(url, file_name, **kwargs)
        self.chunk_count = chunk_count
        self.high_speed = kwargs.get("high_speed", True)
        headers = kwargs.get("headers")
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

        self.__state = _Downloader.INIT
        self.__subs = []

        self.__progress_lock = threading.Lock()

        self.__async = True
        self.thread = threading.Thread(target=self.run)

    # 暂时无用：未实现完整
    def subscribe(self, sub_callable, rate=1):
        self.__subs.append([sub_callable, rate])

    # 暂时无用：未实现完整
    def notify_subs(self, force=False):

        if force:
            self.total_downloaded = 0
            for chunk in self.__chunks:
                self.total_downloaded += chunk.progress

            self.speed = self.total_downloaded - self.last_total
            self.readable_speed = readable_bytes(self.speed)
            self.last_total = self.total_downloaded
        for sub in self.__subs:
            if self.speed > (sub[1] * 1024) or force:
                sub[0](self)

    def get_state(self):
        return self.__state

    def speed_func(self):
        while self.__state != _Downloader.STOPPED and self.__state != _Downloader.MERGING:
            self.total_downloaded = 0
            for chunk in self.__chunks:
                self.total_downloaded += chunk.progress

            self.speed = self.total_downloaded - self.last_total
            self.readable_speed = readable_bytes(self.speed)
            self.last_total = self.total_downloaded

            self.notify_subs()
            time.sleep(1)

    def stop(self):
        for chunk in self.__chunks:
            chunk.stop()
        self.__state = _Downloader.STOPPED

    def start(self):
        if self.__state != _Downloader.INIT:
            raise RuntimeError('Download has already been started.')

        self.thread.start()

    def start_sync(self):
        if self.__state != _Downloader.INIT:
            raise RuntimeError('文件下载已经开始')

        self.run()

    def pause(self):
        if self.__state == _Downloader.INIT:
            print("文件下载尚未开始")
            return

        for chunk in self.__chunks:
            chunk.pause()

        self.__state = _Downloader.PAUSED

    def resume(self):
        if self.__state != _Downloader.PAUSED:
            print("Resume is not applicable at this stage.")
            return
        for chunk in self.__chunks:
            chunk.resume()

        self.__state = _Downloader.DOWNLOADING

    def wait_for_finish(self):
        if self.__async:
            while self.thread.isAlive():
                continue
            self.thread.join()
        else:
            print('Downloader设置为同步，此调用无效')

    def run(self):
        self.__state = _Downloader.DOWNLOADING

        # 为了方便此处用get的stream模式（而非HEAD请求requests.head()）
        r = requests.get(self.url, stream=True, headers=self.headers)
        if r.status_code != 200:
            raise RuntimeError(f'无法正常访问URL:{self.url}')
        try:  # 判断Accept-Ranges
            self.total_length = int(r.headers.get('Content-Length'))  # 获取资源size
            if r.headers.get('Accept-Ranges') != 'bytes':
                raise RuntimeError('URL不支持Range请求')
        except:  # 当资源不支持Range请求的时候直接进行单一请求
            self.chunk_count = 0
        # print("size:", self.total_length)
        if self.chunk_count == 0:
            chunk_file = tempfile.TemporaryFile()
            new_chunk = DownloadChunk(self, self.url, file=chunk_file, high_speed=self.high_speed,
                                      headers=self.headers)
            self.__chunks.append(new_chunk)
            new_chunk.start()
        else:
            # 每块儿大小 = 总大小/分块个数
            chunk_size = self.total_length / self.chunk_count

            for chunk_number in range(self.chunk_count):  # 每块儿分开下载
                chunk_file = tempfile.TemporaryFile()

                if chunk_number != self.chunk_count - 1:  # 是否为最后一块儿
                    new_chunk = DownloadChunk(
                        self, self.url, chunk_file,
                        start_byte=chunk_number * chunk_size,
                        end_byte=((chunk_number + 1) * chunk_size) - 1,
                        number=chunk_number,
                        high_speed=self.high_speed,
                        headers=self.headers)
                else:
                    new_chunk = DownloadChunk(
                        self, self.url, chunk_file,
                        start_byte=chunk_number * chunk_size,
                        end_byte=self.total_length - 1,
                        number=chunk_number,
                        high_speed=self.high_speed,
                        headers=self.headers)

                self.__chunks.append(new_chunk)
                new_chunk.start()

        speed_thread = threading.Thread(target=self.speed_func)
        speed_thread.start()

        for chunk in self.__chunks:
            chunk.thread.join()

        if self.__state == _Downloader.STOPPED:
            return

        # 暂时无用
        self.notify_subs(True)

        self.__state = _Downloader.MERGING
        speed_thread.join()

        # 所有分块儿merge到一起 (wb -> ab?)
        with open(self.file_name, 'wb') as fout:
            for chunk in self.__chunks:
                # seek到临时文件的第一个字节（这一部分可以单独提取filechunkio）
                chunk.file.seek(0)
                while True:
                    readbytes = chunk.file.read(1024 * 1024 * 10)
                    self.total_merged += len(readbytes)
                    if readbytes:
                        fout.write(readbytes)
                        self.notify_subs(force=True)
                    else:
                        break
                chunk.file.close()

        self.__state = _Downloader.FINISHED


def __download(url, file_name=None, chunk_count=8):
    """

    :param url:
    :param file_name:
    :param chunk_count:
    """
    _Downloader(url, file_name, chunk_count).run()
