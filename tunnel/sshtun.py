from os import environ
from subprocess import Popen

class Tunnel:
	"""
	Representation of processes on the OS which are acting as SSH tunnels.

	Raises `OSError` if `dig` command fails.
	"""

	MODE = "-R"

	def __init__(self, **props) -> None:
		self.REMOTE_USER = props["REMOTE_USER"]
		self.REMOTE_HOST = props["REMOTE_HOST"]
		self.ACCESS_PORT = props["ACCESS_PORT"]
		self.SSHKEY_FILE = props["SSHKEY_FILE"]

		self.TUNNEL_PORT = props["TUNNEL_PORT"]
		self.TARGET_HOST = props["TARGET_HOST"]
		self.TARGET_PORT = props["TARGET_PORT"]

		if props["TUNNEL_MODE"] != None:
			self.MODE = props["TUNNEL_MODE"]

	def dig(self):
		command = "ssh -f -N -T"
		command += f" {self.MODE} {self.TUNNEL_PORT}:{self.TARGET_HOST}:{self.TARGET_PORT}"
		command += f" {self.REMOTE_USER}@{self.REMOTE_HOST}"
		command += f" -i {self.SSHKEY_FILE}"
		command += f" -p {self.ACCESS_PORT}"

		hosts = environ.get("KNOWN_HOSTS")
		if hosts != None:
			command += f" -o StrictHostKeyChecking=yes {hosts}"
		else:
			command += f" -o StrictHostKeyChecking=no"

		try:
			self.process = Popen(
				shell=True,
				args=command
			)
		except OSError as e:
			raise OSError(e)

	def terminate(self):
		print(f"[{self.process.pid}] Terminating!")
		try:
			self.process.terminate()
		except OSError:
			self.kill()

	def kill(self):
		print(f"[{self.process.pid}] They want to kill me!")
		try:
			self.process.kill()
		except OSError:
			print("Couldnt kill")