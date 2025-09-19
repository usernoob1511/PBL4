import ftplib
import os
from django.conf import settings

FTP_SERVER = "172.28.147.151"
FTP_PORT = 2121
FTP_USER = "hiephc"
FTP_PASSWORD = "huuhiep0303"

def upload_file_to_ftp(local_file_path, remote_filename):
    """Upload file to FTP server"""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_SERVER, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASSWORD)
        
        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_filename}', file)
        
        ftp.quit()
        return True, "Upload successful"
    except Exception as e:
        return False, str(e)

def download_file_from_ftp(remote_filename, local_file_path):
    """Download file from FTP server"""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_SERVER, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASSWORD)
        
        with open(local_file_path, 'wb') as file:
            ftp.retrbinary(f'RETR {remote_filename}', file.write)
        
        ftp.quit()
        return True, "Download successful"
    except Exception as e:
        return False, str(e)