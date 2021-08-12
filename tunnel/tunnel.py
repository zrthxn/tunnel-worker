from time import time
from threading import Thread, Event
from os import environ
from typing import List
from config import build_satellites
from satellite import Satellite

class setInterval:
	def __init__(self, interval, action, **kwargs):
		self.interval = interval
		self.action = action
		self.kwargs = kwargs
		self.stopEvent = Event()

		Thread(target=self.__setInterval).start()

	def __setInterval(self):
		nextTime = time() + self.interval
		while not self.stopEvent.wait(nextTime - time()):
			nextTime += self.interval
			self.action(**self.kwargs)

	def cancel(self):
		self.stopEvent.set()


def main(satellites: List[Satellite]):
	print("Checking all satellites...")
	for sat in satellites:
		print(f"PING satellite {sat.REMOTE_USER}@{sat.REMOTE_HOST}")
		if sat.ping() == sat.FAIL_STATUS:
			sat.relaunch()

	return 0

if __name__ == "__main__":
	print("Building satellites...")
	satellites = build_satellites()
	print(f"Built {len(satellites)} satellites")

	__time = 3600
	if environ.get("PING_INTERVAL") != None:
		__time = int(environ.get("PING_INTERVAL"))

	if len(satellites) > 0:
		for sat in satellites:
			sat.launch()
		interval = setInterval(__time, main, satellites=satellites)
	else:
		raise RuntimeError("No Satellites Built")