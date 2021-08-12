from subprocess import run

class Tunnel:
	"""
	Representation of processes on the OS which are acting as SSH tunnels.

	Raises `OSError` if `dig` command fails.
	"""

	MODE = "-R"

	def __init__(self, **props) -> None:
		self.REMOTE_HOST = props["REMOTE_HOST"]
		self.ACCESS_PORT = props["ACCESS_PORT"]
		self.SSHKEY_FILE = props["SSHKEY_FILE"]

		self.TUNNEL_PORT = props["TUNNEL_PORT"]
		self.TARGET_HOST = props["TARGET_HOST"]
		self.TARGET_PORT = props["TARGET_PORT"]

		if props["MODE"] is not None:
			self.MODE = props["MODE"]

	def dig(self):
		try:
			self.process = run([
				"ssh", "-f", "-N", "-T", self.MODE,
				f"{self.TUNNEL_PORT}:{self.TARGET_HOST}:{self.TARGET_PORT}",
				"-i", self.SSHKEY_FILE,
				"-p", self.ACCESS_PORT,
			])
		except OSError as e:
			raise OSError(e)

	def kill(self):
		print(f"[{self.process.pid}] They want to kill me!")
		try:
			self.process.kill()
		except OSError:
			print("Couldnt kill")