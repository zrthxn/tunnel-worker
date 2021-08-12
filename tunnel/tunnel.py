from time import time
from threading import Thread, Event
from os import environ
from typing import List
from config import build_satellites
from satellite import Satellite

class setInterval :
	def __init__(self, interval, action):
		self.interval = interval
		self.action = action
		self.stopEvent = Event()

		Thread(target=self.__setInterval).start()

	def __setInterval(self):
		nextTime = time() + self.interval
		while not self.stopEvent.wait(nextTime - time()):
			nextTime += self.interval
			self.action()

	def cancel(self):
		self.stopEvent.set()


def main(satellites: List[Satellite]):
	print("Checking all satellites")
	for sat in satellites:
		print(f"Satellite {sat.REMOTE_HOST}")
		if not sat.is_launched:
			sat.launch()
		elif sat.ping() == sat.FAIL_STATUS:
			sat.relaunch()

	return 0

if __name__ == "__main__":
	satellites = build_satellites()

	__time = 3600
	if environ.get("PING_INTERVAL") != None:
		__time = int(environ.get("PING_INTERVAL"))

	def action():
		main(satellites)

	if len(satellites) > 0:
		interval = setInterval(__time, action)
	else:
		raise RuntimeError("No Satellites Built")