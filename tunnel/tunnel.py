import time, threading
from config import build_satellites

class setInterval :
	def __init__(self, interval, action) :
		self.interval = interval
		self.action = action
		self.stopEvent = threading.Event()

		threading.Thread(target=self.__setInterval).start()

	def __setInterval(self) :
		nextTime = time.time() + self.interval
		while not self.stopEvent.wait(nextTime - time.time()) :
			nextTime += self.interval
			self.action()

	def cancel(self) :
		self.stopEvent.set()


def main():
	for sat in satellites:
		if sat.ping() == sat.FAIL_STATUS:
			sat.relaunch()

	return

if __name__ == "__main__":
	global satellites
	satellites = build_satellites()

	if len(satellites) > 0:
		interval = setInterval(60, main)
	else:
		exit(1)


satellites = []