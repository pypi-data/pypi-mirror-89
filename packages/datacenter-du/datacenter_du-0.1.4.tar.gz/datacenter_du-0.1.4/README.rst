================================
Datacenter Downloader & Uploader
================================


Datacenter Downloader & Uploader



Features
--------

* 数据下载
* 数据上传

Usage
-----

**下载**

一种形式::

  from datacenter_du import Downloader,SimpleDownloader
  Downloader().run()
  SimpleDownloader().run()


另外一种形式::

  from datacenter_du import download,simple_download
  download()
  simple_download()



**上传**

由于

* 由于multi-part-upload需要和server配合
* Content-Range分块上传不适合S3,暂时放弃

目前SimpleUploader,simple_upload可以正常工作，但S3Uploader需要服务端配合
