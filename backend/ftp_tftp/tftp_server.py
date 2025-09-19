
# Simple TFTP server using tftpy
import os
from tftpy import TftpServer

def run_tftp_server():
	upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/media/uploads'))
	os.makedirs(upload_dir, exist_ok=True)
	server = TftpServer(upload_dir)
	print(f"TFTP server running on port 6969, upload dir: {upload_dir}")
	server.listen('0.0.0.0', 6969)

if __name__ == "__main__":
	run_tftp_server()
