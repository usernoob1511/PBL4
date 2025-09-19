import tftpy
import os

TFTP_SERVER = "172.28.147.151"
TFTP_PORT = 6969

def upload_file_to_tftp(local_file_path, remote_filename):
    """Upload file to TFTP server"""
    try:
        client = tftpy.TftpClient(TFTP_SERVER, TFTP_PORT)
        client.upload(remote_filename, local_file_path)
        return True, "Upload successful"
    except Exception as e:
        return False, str(e)

def download_file_from_tftp(remote_filename, local_file_path):
    """Download file from TFTP server"""
    try:
        client = tftpy.TftpClient(TFTP_SERVER, TFTP_PORT)
        client.download(remote_filename, local_file_path)
        return True, "Download successful"
    except Exception as e:
        return False, str(e)