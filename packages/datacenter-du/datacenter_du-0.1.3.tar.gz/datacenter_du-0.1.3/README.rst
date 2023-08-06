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

* 由于multi-part-upload需要和server配合，暂时只提供simple-upload
* Content-Range分块上传不适合S3,暂时放弃

目前只提供了SimpleUploader,simple_upload
