from typing import List
from yaml import load, loader
from os import environ
from satellite import Satellite

yml = """
version: '3.7'
satellites:
  nastunnel:
    REMOTE_USER: "ubuntu"
    REMOTE_HOST: "13.232.166.105"
    ACCESS_PORT: 2020
    SSHKEY_FILE: "../autossh_id_rsa"
    TUNNEL_PORT: 8000

    TUNNEL_MODE: "-R"
    TARGET_HOST: "10.0.0.100"
    TARGET_PORT: 5500
    REMOTE_PING_PORT: 80
    REMOTE_PING_VERB: "GET"
    FAIL_STATUS: 502
"""

def build_satellites() -> List[Satellite]:
	config_path = "" # environ.get("CONFIG_FILE")

	if config_path != None:
		# with open(config_path) as f:
		# config = load(f, Loader=loader.SafeLoader)
		config = load(yml, Loader=loader.SafeLoader)
		satellites = config["satellites"]
		built = []

		for sat in satellites.keys():
			built.append(
				Satellite(
					REMOTE_USER=satellites[sat]["REMOTE_USER"],
					REMOTE_HOST=satellites[sat]["REMOTE_HOST"],
					ACCESS_PORT=satellites[sat]["ACCESS_PORT"],
					SSHKEY_FILE=satellites[sat]["SSHKEY_FILE"],
					TUNNEL_PORT=satellites[sat]["TUNNEL_PORT"],

					TUNNEL_MODE=satellites[sat]["TUNNEL_MODE"],
					TARGET_HOST=satellites[sat]["TARGET_HOST"],
					TARGET_PORT=satellites[sat]["TARGET_PORT"],
					REMOTE_PING_PORT=satellites[sat]["REMOTE_PING_PORT"],
					REMOTE_PING_VERB=satellites[sat]["REMOTE_PING_VERB"],
					FAIL_STATUS=satellites[sat]["FAIL_STATUS"],
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
		