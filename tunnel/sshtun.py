import os

class Tunnel:
	"""
	Representation of processes on the OS which are acting as SSH tunnels.

	Raises `OSError` if `ssh` command fails.
	"""

	MODE = "-R"
	PID = 000

	def __init__(self, **props: dict) -> None:
		self.REMOTE_HOST = props["REMOTE_HOST"]
		self.ACCESS_PORT = props["ACCESS_PORT"]
		self.SSHKEY_FILE = props["SSHKEY_FILE"]

		self.TUNNEL_PORT = props["TUNNEL_PORT"]
		self.TARGET_HOST = props["TARGET_HOST"]
		self.TARGET_PORT = props["TARGET_PORT"]

	def ssh(self):
		try:
			self.pid = os.exec(
				f"ssh -f -N -T {self.MODE}" + 
				f" {self.TUNNEL_PORT}:{self.TARGET_HOST}:{self.TARGET_PORT}" +
				f" -i {self.SSHKEY_FILE}" +
				f" -p {self.ACCESS_PORT}"
			)
		except OSError as e:
			raise OSError(e)

	def kill(self):
		print("They want to kill me!")
		try:
			os.exec(f"kill -9 {self.PID}")
		except OSError:
			print('Couldnt kill')