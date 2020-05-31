# Epic Shell
Just a dumb project to better my coding skills. The goal was to create a webshell that isn't a pain to work with, and one that won't get immediately detected by IPS solutions (work in progress).

## Usage

```
usage: beta.py [-h] [-c CONNECT] [-k KEY] [-g] [-pk PKEY]

Web Shell

optional arguments:
  -h, --help                     Show this help message and exit.
  -c CONNECT, --connect CONNECT  URL of web shell to connect to.
  -k KEY, --key KEY              Auth key for the generated web shell.
  -g, --generate                 Generate new key and webshell.
  -pk PKEY, --payload-key PKEY   Payload key for webshell.
```

### Examples

![screenshot](/images/generate.PNG)

Use the `-g` option to generate a web shell and an accompanying authentication key. There's probably a sneakier way to do it, but this currently requires a specific cookie header to interact with. 

![screenshot](/images/shell.PNG)

Alternatively, if you have the generated shell loaded onto a server, you can interact with it by specifying the `--connect <URL>`, `-k KEY`, and `-pk PAYLOAD_KEY` arguments. If you have trouble connecting, try wrapping the keys in double-quotes on your terminal. This shell supports terminal clearing via the "clear" command. There may be some risks with using `os.system` to do this, but w/e. Baby project, don't care at the moment. 

Payload traffic is base64 & XOR encoded. The session HMAC and XOR schemes are polymorphic, and the values will change everytime you generate a shell. I will try to make this beefier as I get better with PHP. Enjoy!

![screenshot](/images/error.PNG)

Anyone trying to access the shell without the accompanying keys should see this page (might need some work to make it more believable).
