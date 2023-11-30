#!/usr/bin/python3
import random,base64,urllib.parse,zipfile
from globe import zip_tmp

#This config is used to allow setting values that are needed by encoding modules,
#such as the "zip" module needing a zipfile
encoding_configs={"zipfile":None}

#--------------------------#
#    Encoding functions    #
#--------------------------#
def urlEncode(data:bytes)->bytes:
	return urllib.parse.quote_plus(data).encode()

def base64Encode(data:bytes)->bytes:
	return base64.b64encode(data)

def zipEncode(data:bytes)->bytes:
	filename="payload"

	#Write the payload first
	with zipfile.ZipFile(zip_tmp,'w') as a:
		a.writestr(encoding_configs["zipfile"],data)

	#Read the bytes and return them
	with open(zip_tmp,'rb') as f:
		return f.read()

#--------------------#
#    Function Map    #
#--------------------#
encoding_map={"url":urlEncode,
							"base64":base64Encode,
							"zip":zipEncode}