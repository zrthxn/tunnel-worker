from typing import List
from yaml import load, loader
from os import environ
from satellite import Satellite

def build_satellites() -> List[Satellite]:
	config_path = environ.get("CONFIG_FILE")

	if config_path != None:
		with open(config_path) as f:
			config = load(f, Loader=loader.SafeLoader)
			satellites = config["satellites"]
			built = []

			for sat in satellites.keys():
				dic = satellites[sat]
				built.append(
					Satellite(
						REMOTE_USER=key_or_none(dic, "REMOTE_USER"),
						REMOTE_HOST=key_or_none(dic, "REMOTE_HOST"),
						ACCESS_PORT=key_or_none(dic, "ACCESS_PORT"),
						SSHKEY_FILE=key_or_none(dic, "SSHKEY_FILE"),
						TUNNEL_PORT=key_or_none(dic, "TUNNEL_PORT"),

						TUNNEL_MODE=key_or_none(dic, "TUNNEL_MODE"),
						TARGET_HOST=key_or_none(dic, "TARGET_HOST"),
						TARGET_PORT=key_or_none(dic, "TARGET_PORT"),
						REMOTE_PING_PORT=key_or_none(dic, "REMOTE_PING_PORT"),
						REMOTE_PING_VERB=key_or_none(dic, "REMOTE_PING_VERB"),
						FAIL_STATUS=key_or_none(dic, "FAIL_STATUS"),
					)
				)

			return built

	elif environ.get("REMOTE_USER") != None:
		return [
			Satellite(
				REMOTE_USER=environ.get("REMOTE_USER"),
				REMOTE_HOST=environ.get("REMOTE_HOST"),
				ACCESS_PORT=environ.get("ACCESS_PORT"),
				SSHKEY_FILE=environ.get("SSHKEY_FILE"),
				TUNNEL_PORT=environ.get("TUNNEL_PORT"),

				TUNNEL_MODE=environ.get("TUNNEL_MODE"),
				TARGET_HOST=environ.get("TARGET_HOST"),
				TARGET_PORT=environ.get("TARGET_PORT"),
				REMOTE_PING_PORT=environ.get("REMOTE_PING_PORT"),
				REMOTE_PING_VERB=environ.get("REMOTE_PING_VERB"),
				FAIL_STATUS=environ.get("FAIL_STATUS"),
			)
		]
	else:
		return []
		
def key_or_none(dict: dict, key: str):
	try:
		return dict[key]
	except KeyError:
		return None