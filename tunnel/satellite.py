from http import HTTPStatus, client
from sshtun import Tunnel

class Satellite:
	"""
	Representation of all remote hosts from/to which tunnels are made.
	
	Raises `OSError` if `launch` command fails.
	"""
	TARGET_HOST = "localhost"
	TARGET_PORT = 80
	REMOTE_PING_PORT = 80 
	REMOTE_PING_VERB = "GET"
	FAIL_STATUS = HTTPStatus.BAD_GATEWAY[0]

	is_launched = False

	def __init__(self, **props) -> None:
		self.REMOTE_HOST = props["REMOTE_HOST"]
		self.ACCESS_PORT = props["ACCESS_PORT"]
		self.SSHKEY_FILE = props["SSHKEY_FILE"]
		self.TUNNEL_PORT = props["TUNNEL_PORT"]

		self.TARGET_HOST = props["TARGET_HOST"]
		self.TARGET_PORT = props["TARGET_PORT"]

		if props["TARGET_HOST"] is not None:
			self.TARGET_HOST = props["TARGET_HOST"]
		if props["TARGET_PORT"] is not None:
			self.TARGET_PORT = props["TARGET_PORT"]

		if props["REMOTE_PING_PORT"] is not None:
			self.REMOTE_PING_PORT = props["REMOTE_PING_PORT"]
		if props["REMOTE_PING_PORT"] is not None:
			self.REMOTE_PING_VERB = props["REMOTE_PING_VERB"]

		if props["FAIL_STATUS"] is not None:
			self.FAIL_STATUS = int(props["FAIL_STATUS"])
			
	def launch(self):
		try:
			self.tunnel = Tunnel(
				REMOTE_HOST=self.REMOTE_HOST,
				ACCESS_PORT=self.ACCESS_PORT,
				SSHKEY_FILE=self.SSHKEY_FILE,

				TUNNEL_PORT=self.TUNNEL_PORT,
				TARGET_HOST=self.TARGET_HOST,
				TARGET_PORT=self.TARGET_PORT,
			)
			self.tunnel.dig()
			self.is_launched = True
		except OSError as e:
			raise OSError(e)

	def ping(self):
		c = client.HTTPConnection(self.REMOTE_HOST, int(self.REMOTE_PING_PORT))
		if int(self.REMOTE_PING_PORT) == 443:
			c = client.HTTPSConnection(self.REMOTE_HOST, 443)
		try:
			c.request(self.REMOTE_PING_VERB, "/")
			r = c.getresponse()
			return r.getcode()
		except ConnectionError:
			return self.FAIL_STATUS

	def relaunch(self):
		self.tunnel.kill()
		self.is_launched = False
		self.launch()
	