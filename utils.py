import os, sys, configparser, shutil, subprocess


def PathWinToUnix(src):
	drive=src.split(':' ,maxsplit=1)
	path=src.split('\\')
	del(path[0])
	path.insert(0, 'cygdrive')
	path.insert(1, drive[0].lower())
	
	for i in range(len(path)):
		path[i]='/'+path[i]
		if (i==len(path)-1): path[i]=path[i]+'/'
	
	res = ''.join(path)
	return res

def getHomeDirPath():
	from os.path import expanduser
	home = expanduser("~")
	return home


def getConfigDirPath():
	from os.path import expanduser
	home = expanduser("~")
	if sys.platform == 'win32': 
		configDir=home+"\\AppData\\Local\\pobkup\\"
	elif  sys.platform == 'linux':
		configDir=home+"/.config/pobkup/"
	elif sys.platform== "darwin":
		configDir=home+"/.config/pobkup/"	
	else:
		configDir=home+"/.config/pobkup/"
	
	return configDir	

def getProfilesFilePath():
	p=getConfigDirPath()+"profiles.conf"
	return p
	

def initConfig():
	confDir=getConfigDirPath()
	profilesFile=getProfilesFilePath()
	
	if (not os.path.isdir(confDir)):
		os.makedirs(confDir)
	if (not os.path.isfile(profilesFile)):
		config = configparser.ConfigParser()
		config.add_section('backup')
		config['backup']['src'] = getHomeDirPath()
		config['backup']['dst'] = ""
		config['backup']['delete'] = "yes"
		config['backup']['history'] = "no"
		config['backup']['service'] = "no"
		config['backup']['dayofweek'] = ""
		config['backup']['excludeFile'] = ""
		config['backup']['time'] = ""
		config['backup']['lastbackup'] = ""
		with open(profilesFile, 'w') as configfile:
			config.write(configfile)

def getRsyncPath():
	rsync=None
	if  sys.platform == 'linux':
		rsync=shutil.which("rsync")
	elif sys.platform == 'win32':
		if getattr(sys, 'frozen', False):
			# frozen
			rsync= os.path.join(os.path.dirname(sys.executable),"win32rsync","rsync.exe")
		else:
			# unfrozen
			rsync=os.path.join(os.path.dirname(os.path.realpath(__file__)),"win32rsync","rsync.exe")	
	elif sys.platform== "darwin":
		rsync=shutil.which("rsync")
	else:
		rsync=shutil.which("rsync")
	return rsync
	
def checkPath(p):
	if (not os.path.isdir(p)):
		return False
	else:
		return True	

def getTimeHistoryFolder():
	import datetime
	now = datetime.datetime.now()
	d= "%d-%d-%d_%d.%d.%d%s" % ( now.year,  now.month, now.day, now.hour, now.minute, now.second,os.sep)
	return '/'+d

def getTempDir():
	import tempfile
	return tempfile.gettempdir()+os.sep

def poweroff():
	if  sys.platform == 'linux':
		subprocess.call(["systemctl", "poweroff"])
	if sys.platform=="win32":
		subprocess.call(["shutdown", "/s"])
	if sys.platform == "darwin":
		subprocess.call(['osascript', '-e','tell app "System Events" to shut down'])	
		
