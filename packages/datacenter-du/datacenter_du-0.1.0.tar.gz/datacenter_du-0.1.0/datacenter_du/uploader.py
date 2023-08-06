"""数据上传
by tacey@XARC on 2020/12/22
"""

import os
import time
import shutil
import tempfile
import logging
import subprocess
import threading
import requests
from requests import Session

from .transfer import Chunk, readable_bytes


class UploaderBase:
    def __init__(self):
        raise NotImplemented

    def run(self):
        raise NotImplemented


class UploadChunk(Chunk):

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
            self.upload_iter_size = 1024 * 512  # 0.4 M
        else:
            self.upload_iter_size = 1024  # 1K

    def read_in_chunks(self, file_object, chunk_size=65536):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def run(self, r=None):
        self.__state = Chunk.DOING
        if r is None:
            pass
        break_flag = False
        content_path = os.path.abspath(self.file)
        content_size = os.stat(content_path).st_size
        f = open(content_path)

        index = 0
        offset = 0
        headers = {}

        for chunk in self.read_in_chunks(f):
            offset = index + len(chunk)
            headers['Content-Type'] = 'application/octet-stream'
            headers['Content-length'] = content_size
            headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, content_size)
            index = offset
            try:
                r = requests.post(url, data=chunk, headers=headers)
                print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
            except Exception:
                pass

        if not break_flag:
            self.__state = Chunk.FINISHED


#
# def read_in_chunks(file_object, chunk_size=65536):
#     while True:
#         data = file_object.read(chunk_size)
#         if not data:
#             break
#         yield data
#
#
# def main(file, url):
#     content_name = str(file)
#     content_path = os.path.abspath(file)
#     content_size = os.stat(content_path).st_size
#
#     print(content_name, content_path, content_size)
#
#     f = open(content_path)
#
#     index = 0
#     offset = 0
#     headers = {}
#
#     for chunk in read_in_chunks(f):
#         offset = index + len(chunk)
#         headers['Content-Type'] = 'application/octet-stream'
#         headers['Content-length'] = content_size
#         headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, content_size)
#         index = offset
#         try:
#             r = requests.put(url, data=chunk, headers=headers)
#             print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
#         except Exception:
#             pass


class SimpleUploader:

    def __init__(self, url, file_path, file_name, fields=None, headers=None, **kwargs):
        self.url = url
        self.file_path = file_path
        self.fields = fields
        self.headers = headers
        self.file_name = file_name

    def run(self):
        with Session() as session:
            with open(self.file_path, "rb") as f:
                file_field = {'file': (self.file_name, f)}
                session.post(self.url, data=self.fields, files=file_field)


class CURLUploader:

    def __init__(self, url, file_path, file_name, fields=None, **kwargs):
        self.url = url
        self.file_path = file_path
        self.file_name = file_name
        self.fields = ""
        if fields is not None:
            self.fields = " ".join([f'-F "{k}={v}"' for k, v in fields.items()])

    def run(self):
        curl = os.getenv("CURL_PATH")
        curl = curl if curl else shutil.which("curl")
        if not curl:
            if not os.getenv("USE_SIMPLE_IF_CURL_NOT_EXIST"):
                raise RuntimeError("数据上传依赖curl"
                                   "如果curl未在系统PATH路径下，请配置CURL_PATH环境变量。")
            else:

                logging.warning("使用本地简单")
                return Uploader(url=self.url, file_=self.file_path).run()
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        # 注意：-F file字段必须放在最后，S3会忽略file字段之后的所有字段
        result = subprocess.run(
            [shutil.which("sh"), "-c",
             f'{curl} -k {self.fields} -F "file=@{self.file_path}"  "{self.url}" -i > /dev/null'],
            stderr=subprocess.PIPE)
        if result.returncode != 0:
            logging.exception(result.stderr)
        return not (bool(result.returncode))


class Uploader:
    # 文件下载状态
    INIT = 0
    UPLOADING = 1
    PAUSED = 2
    MERGING = 3
    FINISHED = 4
    STOPPED = 5

    def __init__(self, url, file_, chunk_count=None, high_speed=False, headers=None):
        self.url = url
        self.file_ = file_
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
        self.total_uploaded = 0
        self.total_merged = 0
        self.__chunks = []

        self.last_total = 0
        self.speed = 0
        self.readable_speed = readable_bytes(self.speed)

        self.__state = Uploader.INIT
        self.__subs = []

        self.__progress_lock = threading.Lock()

        self.__async = True
        self.thread = threading.Thread(target=self.run)

    def get_state(self):
        return self.__state

    def speed_func(self):
        while self.__state != Uploader.STOPPED:
            self.total_uploaded = 0
            for chunk in self.__chunks:
                self.total_uploaded += chunk.progress

            self.speed = self.total_downloaded - self.last_total
            self.readable_speed = readable_bytes(self.speed)
            self.last_total = self.total_downloaded

            time.sleep(1)

    def stop(self):
        for chunk in self.__chunks:
            chunk.stop()
        self.__state = Uploader.STOPPED

    def start(self):
        if self.__state != Uploader.INIT:
            raise RuntimeError('上传已经开始.')
        self.thread.start()

    def run(self):
        self.__state = Uploader.UPLOADING
        content_path = os.path.abspath(self.file_)
        self.total_length = os.stat(content_path).st_size  # 获取资源size
        if self.chunk_count is None:
            self.chunk_count = 0

        if self.chunk_count == 0:
            new_chunk = UploadChunk(self, self.url, file=self.file_, high_speed=self.high_speed,
                                    headers=self.headers)
            self.__chunks.append(new_chunk)
            new_chunk.start()
        else:
            # 每块儿大小 = 总大小/分块个数
            chunk_size = self.total_length / self.chunk_count

            for chunk_number in range(self.chunk_count):  # 每块儿分开下载
                chunk_file = tempfile.TemporaryFile()

                if chunk_number != self.chunk_count - 1:  # 是否为最后一块儿
                    new_chunk = UploadChunk(
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

        if self.__state == Uploader.STOPPED:
            return

        self.notify_subs(True)

        self.__state = Uploader.MERGING
        speed_thread.join()

        # 所有分块儿merge到一起 (wb -> ab?)
        pass

        self.__state = Uploader.FINISHED


if __name__ == '__main__':
    file_path = "/home/tacey/PycharmProjects/datacenter/README.rst"
    url = "https://xarc-datacenter.s3.cn-northwest-1.amazonaws.com.cn/"
    fields = {'key': 'bbr.sh', 'x-amz-algorithm': 'AWS4-HMAC-SHA256',
              'x-amz-credential': 'AKIA5YRY5HWNPM4RTU6S/20201208/cn-northwest-1/s3/aws4_request',
              'x-amz-date': '20201208T090428Z',
              'policy': 'eyJleHBpcmF0aW9uIjogIjIwMjAtMTItMDhUMTA6MDQ6MjhaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAieGFyYy1kYXRhY2VudGVyIn0sIHsia2V5IjogImJici5zaCJ9LCB7IngtYW16LWFsZ29yaXRobSI6ICJBV1M0LUhNQUMtU0hBMjU2In0sIHsieC1hbXotY3JlZGVudGlhbCI6ICJBS0lBNVlSWTVIV05QTTRSVFU2Uy8yMDIwMTIwOC9jbi1ub3J0aHdlc3QtMS9zMy9hd3M0X3JlcXVlc3QifSwgeyJ4LWFtei1kYXRlIjogIjIwMjAxMjA4VDA5MDQyOFoifV19',
              'x-amz-signature': '276192b83f34d49580b57edc3ed0bf9c0a4e695dbefd73677e8168a0c7677b75'}
    CURLUploader(url=url, fields=fields, file_path=file_path, file_name="bbr.sh").run()
