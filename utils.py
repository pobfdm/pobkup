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
		config['backup']['excludeFile'] = ""
		config['backup']['cmdBefore'] = ""
		config['backup']['cmdAfter'] = ""
		config['backup']['logfile'] = ""
		config['backup']['everyMinutes'] = ""
		config['backup']['everyHours'] = ""
		config['backup']['everyDayAt'] = ""
		
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

def notifySend(title, message):
	if getattr(sys, 'frozen', False):
			# frozen
			iconPobkup= os.path.join(os.path.dirname(sys.executable),"icons","icon.png")
			notifySendWin=os.path.join(os.path.dirname(sys.executable),"notify-send","notify-send.exe")
	else:
		# unfrozen
		iconPobkup=os.path.join(os.path.dirname(os.path.realpath(__file__)),"icons","icon.png")
		notifySendWin=os.path.join(os.path.dirname(os.path.realpath(__file__)),"notify-send","notify-send.exe")
		
		
	if  sys.platform == 'linux':
		try:
			subprocess.call(["notify-send", title, message, "--icon="+iconPobkup])
		except:
			print ("Error on notify")
	if sys.platform=="win32":
		try:
			#subprocess.call([notifySendWin, "-i", "info", title, message])
			subprocess.Popen([notifySendWin, "-i", "info", title, message])	
		except:
			print ("Error on notify")
			
			
		
	if sys.platform=="darwin":
		try:
			 os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, title))	
		except:
			print ("Error on notify")

def getAutorunFolder():
	if sys.platform=="win32":
		return getHomeDirPath()+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
	if  sys.platform == 'linux':
		return getHomeDirPath()+"/.config/autostart/"




 
def createWinShortcut(src, link, workingDir, icon):    
	vbscript='''
	Set oWS = WScript.CreateObject("WScript.Shell")
	sLinkFile = "%s"
	Set oLink = oWS.CreateShortcut(sLinkFile)
		oLink.TargetPath = "%s"
	 '  oLink.Arguments = ""
	   oLink.Description = "Pobkupd.  The Pobkup deamon "   
	 '  oLink.HotKey = "ALT+CTRL+F"
	   oLink.IconLocation = "%s, 2"
	 '  oLink.WindowStyle = "1"   
	   oLink.WorkingDirectory = "%s"
	oLink.Save
	''' % (link, src, icon, workingDir)
	path=getTempDir()+'createShortcut.vbs'
	print(vbscript,  file=open(path, 'w'))
	os.system(path)
	
def installPobkupd():
	if  sys.platform == 'linux':
		src="/usr/lib/pobkup/pobkupd.desktop"
		dst=getAutorunFolder()+"pobkupd.desktop"
		try:
			shutil.copyfile(src, dst)
		except:
			pass				
	
	
	if  sys.platform == 'win32':
		if getattr(sys, 'frozen', False):
			# frozen
			src=os.path.join(os.path.dirname(sys.executable),"pobkupd.exe") 
			dst=getAutorunFolder()+"pobkupd.lnk"
			pobkupDir=os.path.join(os.path.dirname(sys.executable))
			icon=os.path.join(os.path.dirname(sys.executable),"pobkupd.exe") 
		else:
			# unfrozen
			src=os.path.join(os.path.dirname(os.path.realpath(__file__)),"pobkupd.py")
			dst=getAutorunFolder()+"pobkupd.lnk"
			pobkupDir=os.path.join(os.path.dirname(os.path.realpath(__file__)))
			icon=sys.executable
		
		createWinShortcut(src,dst,pobkupDir,icon)
		
	if (os.path.isfile(dst)):
		return True
	else:
		return False

def removePobkupd():
	if  sys.platform == 'linux':
		dst=getAutorunFolder()+"pobkupd.desktop"
		if (os.path.isfile(dst)):
			os.remove(dst)	
		if (not os.path.isfile(dst)):
			return True
		else:	
			return False		

	if  sys.platform == 'win32':
		if getattr(sys, 'frozen', False):
			# frozen
			dst=getAutorunFolder()+"pobkupd.lnk"
		else:
			# unfrozen
			dst=getAutorunFolder()+"pobkupd.lnk"
		
		if (os.path.isfile(dst)):
			os.remove(dst)	
		if (not os.path.isfile(dst)):
			os.system("TASKKILL /F /IM pobkupd.exe")
			return True
		else:	
			return False

def checkIsRunning(program):
	import psutil
	for pid in psutil.pids():
		p = psutil.Process(pid)
		if p.name() == program :
			return True
	return False




