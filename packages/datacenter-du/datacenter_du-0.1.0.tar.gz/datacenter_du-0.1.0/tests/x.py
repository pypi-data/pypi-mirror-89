"""
by tacey@XARC on 2020/12/22
"""
import time
from datacenter_du.downloader import download, __download

if __name__ == "__main__":
    start = time.time()
    __download(
        "http://192.168.1.182/download/Microsoft_Office_16.33.20011301_BusinessPro_Installer.pkg")
    print(time.time() - start)
