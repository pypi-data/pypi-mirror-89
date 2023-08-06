"""
by tacey@XARC on 2020/12/22
"""
import time
from datacenter_du.downloader import download, __download
from datacenter_du.uploader import upload, simple_upload, simple_plus_upload,curl_upload

if __name__ == "__main__":
    # start = time.time()
    # __download(
    #     "http://192.168.1.182/download/Microsoft_Office_16.33.20011301_BusinessPro_Installer.pkg")
    # print(time.time()-start)
    start = time.time()
    file_path="/home/tacey/GoWorkspace/src/go-simple-upload-server/server"
    simple_plus_upload(url="https://xarc-datacenter.s3.cn-northwest-1.amazonaws.com.cn/",
                  file_path=file_path,
                file_name="upload.exe",
                fields={'key': 'test_exe', 'x-amz-algorithm': 'AWS4-HMAC-SHA256', 'x-amz-credential': 'AKIA5YRY5HWNPM4RTU6S/20201222/cn-northwest-1/s3/aws4_request', 'x-amz-date': '20201222T114540Z', 'policy': 'eyJleHBpcmF0aW9uIjogIjMxNjEtMTAtMDlUMDM6NDU6NDBaIiwgImNvbmRpdGlvbnMiOiBbeyJidWNrZXQiOiAieGFyYy1kYXRhY2VudGVyIn0sIHsia2V5IjogInRlc3RfZXhlIn0sIHsieC1hbXotYWxnb3JpdGhtIjogIkFXUzQtSE1BQy1TSEEyNTYifSwgeyJ4LWFtei1jcmVkZW50aWFsIjogIkFLSUE1WVJZNUhXTlBNNFJUVTZTLzIwMjAxMjIyL2NuLW5vcnRod2VzdC0xL3MzL2F3czRfcmVxdWVzdCJ9LCB7IngtYW16LWRhdGUiOiAiMjAyMDEyMjJUMTE0NTQwWiJ9XX0=', 'x-amz-signature': 'e4f11cf55d6b9a7ffa8bafa94cfed7c16fc199bf718546b78b64bfc038ab30dc'}
    )
    print(time.time()-start)
    # {'result': {'url': 'https://xarc-datacenter.s3.cn-northwest-1.amazonaws.com.cn/',
    #             'fields': }}

