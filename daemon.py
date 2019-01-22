#!/usr/bin/env python3

from utils import *
import schedule
import time, gettext, locale



#Read Configuration
config = configparser.ConfigParser()
config.read(getProfilesFilePath())
profiles=config.sections()

#Gettext
try:
	current_locale, encoding = locale.getdefaultlocale()
	locale_path = 'locale'
	language = gettext.translation ('pobkup', locale_path, [current_locale] )
	language.install()
except:
	print("Locale not found")
	_ = gettext.gettext 



def startBackup(p):
	
	if (not sys.platform == 'win32'): 
		src=config[p]['src']
		dst=config[p]['dst']
	else:
		src=PathWinToUnix(config[p]['src'])
		dst=PathWinToUnix(config[p]['dst'])	

	rsyncBin=getRsyncPath()
	delete=config.getboolean(p,'delete')
	history=config.getboolean(p,'history')
	excludeFile=config[p]['excludeFile']

	cmd=[rsyncBin, '-avh', '--info=progress2']
	if (delete==True): cmd.append('--delete')
	if (len(excludeFile)>1) : cmd.append("--exclude-from="+excludeFile)
	if (history==True): dst+=getTimeHistoryFolder()
	cmd.append(src)
	cmd.append(dst)
	
	notifySend(_("Starting backup"), config[p].name+ _(" is starting..."))
	print(config[p].name+ _(" is starting..."))
	subprocess.call(cmd)
	notifySend(_("Backup done."), config[p].name+ _(" is done."))
	print(config[p].name+ _(" is done."))


for p in profiles:
	#Minutes
	try:
		if (config[p]['everyMinutes']!=None): schedule.every(int(config[p]['everyMinutes'])).minutes.do(startBackup, p)
	except KeyError:
		print('Key "everyMinutes" of [%s] not found' % str(config[p].name))
	
	#Hours
	try:
		if (config[p]['everyHours']!=None): schedule.every(int(config[p]['everyHours'])).hours.do(startBackup, p)
	except KeyError:
		print('Key "everyHours" of [%s] not found' % str(config[p].name))
	
	#Day at 
	try:
		if (config[p]['everyDayAt']!=None): schedule.every().day.at(config[p]['everyDayAt']).do(startBackup, p)
	except KeyError:
		print('Key "everyDayAt" of [%s] not found' % str(config[p].name))		

#Start scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
