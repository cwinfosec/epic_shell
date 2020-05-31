# Epic Shell
Just a dumb project to better my coding skills. The goal was to create a webshell that isn't a pain to work with, and one that won't get immediately detected by IPS solutions (work in progress).

## Usage

![screenshot](/images/generate.PNG)

Use the `-g` option to generate a web shell and an accompanying authentication key. There's probably a sneakier way to do it, but this currently requires a specific cookie header to interact with. 

![screenshot](/images/shell.PNG)

Alternatively, if you have a shell loaded onto a server, you can interact with it by specifying the `--connect <URL>` and `-k KEY` arguments. This shell supports terminal clearing via the "clear" command. There may be some risks with using `os.system` to do this, but w/e. Baby project, don't care at the moment. 

Payload traffic is base64 encoded. I will try to make this beefier as I get better with PHP. Enjoy!