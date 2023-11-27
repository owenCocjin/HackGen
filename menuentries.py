import re
from ProgMenu.progmenu import EntryArg,EntryFlag,EntryPositional
from globe import curse

def helpFunc():
	print("""hackgen.py [-bfhilpuw] <local ip> <local port>
Generate rshell payloads for a given ip and port.
  <local ip>;         Your IP
  <local port>;       Your port
  --ip;               Your IP.
                      Alternate to positional arg
  --port;             Your port.
                      Alternate to positional arg
  -b; --base64;       Base64 encode the payload
  -f; --platform=<p>; Specify platform to get rshell from.
                      Use -l to list all rshells.
  -h; --help;         Print this page
  -i; --id=<id>;      Use id instead of specifying platform and name
                      Ignores -f and -n if called
  -l; --list;         List all rshells.
                      If -f was specified, only list rshells for that platform
  -n; --name=<n>;     Name of the rshell to use
  -u; --urlencode;    URL encode the rshell before outputting it
  -w; --webserver;    Start a webserver that will output the rshell instead of outputting to stdout.
                      This is userful to get the rshell directly onto a target (via curl/wget) instead of sending it as a file, etc...
""")

def ipFunc(i:str):
	'''Get the ip from the user.
	If they don't provide an IP we'll need to get it from somewhere else, like a custom env var?'''
	if not re.fullmatch("^[0-9]+(\.[0-9]+){3}$",i):
		print(f"[|x:menu:ip]: Invalid IP: {i}")
		exit(1)
	return i

def listFunc(p):
	'''List all the payloads.
	If a payload is already specified, list all the subtypes (for example, netcat has a few different ways to do an rshell)'''

	#If the platform was give, list all shells from that 
	if p:
		loop_data=curse.execute("SELECT name,description,data,platform,uid FROM rshells WHERE platform=?",(p,)).fetchall()
	else:
		#Get longest platform name for formatting
		spaces=curse.execute("SELECT MAX(LENGTH(platform)) FROM rshells").fetchall()[0][0]

		#Print all available platforms
		print(f"Available platforms + payload count:")
		for n in curse.execute("SELECT DISTINCT platform FROM rshells ORDER BY platform").fetchall():
			n=n[0]

			#Get number of payloads for the current platform
			payloadcount=curse.execute("SELECT COUNT() FROM rshells WHERE platform=?",(n,)).fetchall()[0][0]
			print(f"  \033[1m{n}{' '*(spaces-len(n))} [{payloadcount}]\033[0m")
		print(f"\n  --- \n")
		loop_data=curse.execute("SELECT name,description,data,platform,uid FROM rshells ORDER BY platform").fetchall()

	for data in loop_data:
		payload=data[2].replace("^LOCAL_IP^",f"""\033[94m<ip>\033[0m""").replace("^LOCAL_PORT^",f"""\033[95m<port>\033[0m""")
		if '\n' in payload:
			printout="\033[90m<multi-line file; redacted>\033[0m"
		elif type(payload)==bytes:
			printout="\033[90m<binary data; redacted>\033[0m"
		elif len(payload)>80:
				printout=f"{payload[:80]}\033[0m..."
		else:
			printout=payload
		print(f"""[{data[4]}] \033[1m{data[3]} - {data[0]}\033[0m:\n\033[3m{data[1]}\033[0m\n  {printout}\n""")

	exit(0)
	return True

def platformFunc(p:str):
	'''Get the type of platform from the user (php, bash, etc...)'''
	#Check that the platform exists in the db.
	if p not in [i[0] for i in curse.execute("SELECT DISTINCT platform FROM rshells").fetchall()]:
		print(f"[|x:menu:platform]: Nothing found for platform: {p}")
		exit(2)

	return p

def portFunc(p:int):
	try:
		if not 1024<int(p)<65535:
			print(f"[|x:menu:port]: Invalid port: {p}")
			exit(1)
	except ValueError:
		print(f"[|x:menu:port]: Invalid port: {p}")
	return p

def idFunc(i):
	'''Make sure the given ID exists in the DB'''
	if not curse.execute(f"SELECT id FROM rshells WHERE uid=?",(i,)).fetchall():
		print(f"[|x:idFunc]: Invalid id: {i}")
		exit(1)

	return i


EntryFlag("help",['h',"help"],helpFunc)
EntryArg("ip_flag",["ip"],ipFunc)
EntryArg("id",['i',"id"],idFunc)
EntryFlag("base64encode",['b',"base64"],lambda:True)
EntryFlag("list",['l',"list"],listFunc,recurse=["platform"])
EntryArg("name",['n',"name"],lambda n:n,strictif=["list","id"])
EntryArg("platform",['f',"platform"],platformFunc,strictif=["list","id"])
EntryArg("port_flag",["port"],portFunc,default=3184)
EntryFlag("urlencode",['u',"urlencode"],lambda:True)
EntryFlag("web",['w',"web","webserver","server"],lambda:True)
EntryPositional("ip",0,ipFunc,alt=["ip_flag"])
EntryPositional("port",1,portFunc,alt=["port_flag"])
