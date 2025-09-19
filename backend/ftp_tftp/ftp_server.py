
# Simple FTP server using pyftpdlib
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def run_ftp_server():
	authorizer = DummyAuthorizer()
	# user: test, password: 12345, full r/w access to uploads
	upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend/media/uploads'))
	os.makedirs(upload_dir, exist_ok=True)
	authorizer.add_user("hiephc", "huuhiep0303", upload_dir, perm="elradfmwMT")
	handler = FTPHandler
	handler.authorizer = authorizer
	handler.passive_ports = range(60000, 65535)
	server = FTPServer(("172.28.147.151", 2121), handler)
	print(f"FTP server running on port 2121, upload dir: {upload_dir}")
	server.serve_forever()

if __name__ == "__main__":
	run_ftp_server()
