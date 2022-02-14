# author: bah0 -> https://github.com/bah0/bahosScriptKit
# version 1.0
# requirements:
# python 3.7+
# pysftp (pip install pysftp)

import os
import sys
import datetime
import pysftp
import logging
from os import walk

#global vars
WORKDIR = os.path.join(os.getcwd(), "upload")
DONEDIR = os.path.join(WORKDIR,"done")
logger = logging.getLogger(__name__)
logFilename = "sendbot.log"

ftpserver='192.168.0.87' # Remote Location
ftpuname='demo' # Username

ftppwd='password' # password is plaintext just for dev/testing purposes. 
				  # !!! DO NOT USE PLAINTEXT PASSWORDS IN PRODUCTION !!!
                  # Use or implement your own methods of securing passwords for production!

remotePath="/testupload/" # Remote Path (optional, leave / for home directory)

# SFTP preconf
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
#
	
def main():	
	setupLogger()
	init()
	uploadFiles()
	
def setupLogger():
	# logger preconf
	logging.basicConfig(level=logging.INFO)
	global logger	
	handler = logging.FileHandler(logFilename)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s :: %(message)s")
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	
def init():	
	logger.info("==== START OF PROGRAM ====")
	logger.debug("current working directory: "+WORKDIR)
	logger.info("SFTP Server: "+ftpserver)
	checkFolders()

def getFiles():
	f = []
	for(dirpath, dirnames, filenames) in walk(WORKDIR):
		f.extend(filenames)
		break
		
	files = [ fi for fi in f if fi.endswith(".csv")]
	logger.debug("CSV files in workdir: "+str(files))
	return files
	
def uploadFiles():
	with pysftp.Connection(host=ftpserver,username=ftpuname,password=ftppwd, cnopts=cnopts) as sftp:
		for i in getFiles():
			remoteFile = i
			remoteLocation = os.path.join(remotePath,remoteFile)
			try:
				sftp.stat(remoteLocation)
				logger.info("file exists on server: "+remoteLocation)
				logger.info("moving file in done directory without copying to server")				
			except IOError:
				logger.info(WORKDIR+"\\"+i + " --> "+ ftpserver + remoteLocation)
				sftp.put(os.path.join(WORKDIR,i),remoteLocation)
			
			try:
				os.rename(os.path.join(WORKDIR,i),os.path.join(DONEDIR,i))
			except FileExistsError:
				localFile = datetime.datetime.now().strftime("%Y-%m-%d - %H.%M.%S") +" "+ i
				os.rename(os.path.join(WORKDIR,i),os.path.join(DONEDIR,localFile))
		sftp.close()
							
def checkFolders():
	checkWorkdir = os.path.exists(WORKDIR)
	checkDonedir = os.path.exists(DONEDIR)
	logger.debug("folder WORKDIR exists: "+str(checkWorkdir));
	logger.debug("folder DONEDIR exists: "+str(checkDonedir));
	if checkWorkdir == False:
		logger.debug("making directory: "+WORKDIR)
		os.mkdir(WORKDIR)

	if checkDonedir == False:
		logger.debug("making directory: "+DONEDIR)
		os.mkdir(DONEDIR)			
		
if __name__ == "__main__":
	main()		