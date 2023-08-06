"""Top-level package for Datacenter Downloader & Uploader.

https://tools.ietf.org/html/rfc7233
"""

__author__ = """Datacenter Downloader & Uploader"""
__email__ = 'xinyong.wang@xtalpi.com'
__version__ = '0.1.4'

from .downloader import Downloader, download, SimpleDownloader, simple_download
from .uploader import SimpleUploader, simple_upload

__all_ = ["Downloader", "download", "SimpleDownloader", "simple_download", "SimpleUploader",
          "simple_upload"]
