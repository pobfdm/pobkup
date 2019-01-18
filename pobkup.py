#!/usr/bin/env python3
import wx, threading, gettext, configparser, sys, subprocess, shlex,os
from gui_utils import *
from wx import xrc

import utils, gui_utils
from profiles import *

class MainApp(wx.App):
	
	currProfile=None
	imWorking=False

	def OnInit(self):
		self.res = xrc.XmlResource(os.path.join('gui','mainFrame.xrc'))
		self.init_frame()
		return True

	def init_frame(self):
		self.proc=None
		self.frame = self.res.LoadFrame(None, 'mainFrame')
		self.frame.SetIcon(wx.Icon("icon.ico"))
		self.btBackup = xrc.XRCCTRL(self.frame, 'btBackup')
		self.lstOutput= xrc.XRCCTRL(self.frame, 'lstOutput')
		self.cmbProfiles=xrc.XRCCTRL(self.frame, 'cmbProfiles')
		self.btEditProfile=xrc.XRCCTRL(self.frame, 'btEditProfile')
		self.lblStatus=xrc.XRCCTRL(self.frame, 'lblStatus')
		
		#Getting menu
		self.menubar = self.frame.GetMenuBar()
		self.mnuItemExit = self.menubar.FindItemById(xrc.XRCID('mnuItemExit'))
		self.mnuItemNewProfile = self.menubar.FindItemById(xrc.XRCID('mnuItemNewProfile'))    
		#Bind event Menu
		self.frame.Bind(wx.EVT_MENU, self.quit, self.mnuItemExit)
		self.frame.Bind(wx.EVT_MENU, self.newProfiles, self.mnuItemNewProfile)
		
		#Init ListCtrl
		self.lstOutput.InsertColumn(0, "File")
		self.lstOutput.SetColumnWidth(0, -2)
		self.progress=xrc.XRCCTRL(self.frame, 'progress')
		
		
		#Bind events widgets
		self.btBackup.Bind(wx.EVT_BUTTON, self.onStartStop)
		self.cmbProfiles.Bind(wx.EVT_COMBOBOX, self.setProfile)
		self.frame.Bind(wx.EVT_CLOSE, self.quit)
		self.frame.Bind(wx.EVT_ACTIVATE, self.initComboBoxProfiles)
		self.btEditProfile.Bind(wx.EVT_BUTTON, self.editProfile)
		
		#self.initComboBoxProfiles()
		self.frame.Show()
	
	def setStatus(self,s):
		wx.CallAfter(self.lblStatus.SetLabel, s)
	
	def quit(self,evt):
		r= YesNo(self.frame, _("Do you want exit?"), caption = 'Exit')
		if (r==True):
			self.Destroy()
			sys.exit()
			
			
		
	def newProfiles(self,evt):
		print("New profile...")
		pr= Profiles()
		pr.OnInit()
	
	def editProfile(self,evt):
		print("Edit profile...")
		pr= Profiles()
		pr.OnInit()
		pr.setProfile(self.currProfile)
	
	def setProfile(self, evt):
		self.currProfile=self.cmbProfiles.GetValue()
	
	def initComboBoxProfiles(self, evt):
		self.config = configparser.ConfigParser()
		self.config.read(utils.getProfilesFilePath())
		profiles=self.config.sections()
		self.cmbProfiles.Clear()
		for p in profiles:
			self.cmbProfiles.Append(p)
		
		self.cmbProfiles.SetSelection(self.cmbProfiles.GetCount()-1)	
		self.currProfile=self.cmbProfiles.GetValue()
	
	def busyGui(self):
		wx.CallAfter(self.btBackup.SetLabel, "Stop!")
	
	def readyGui(self):
		wx.CallAfter(self.btBackup.SetLabel, "Backup!")
	
	def	appendOutput(self,s):
		count=self.lstOutput.GetItemCount()
		wx.CallAfter(self.lstOutput.InsertItem,count,s)
		wx.CallAfter(self.lstOutput.Focus, count)
	
	def cleanOutput(self):
		wx.CallAfter(self.lstOutput.DeleteAllItems)	
	
	def getPercent(self,line):
		# Example 11,131,595   1%   10.47MB/s    0:00:00 (xfr#16, to-chk=2761/4538)
		line=line.split(" ")
		for l in line:
			if ('%' in l):
				if (len(l)==2): return l[0]
				if (len(l)==3): return l[0]+l[1]
				if (len(l)==4): return l[0]+l[1]+l[2]		
				
	def startStopBackup(self):
		self.imWorking=True
		self.busyGui()
		rsyncBin=utils.getRsyncPath()
		self.config.read(utils.getProfilesFilePath())
		if (not sys.platform == 'win32'): 
			src=self.config[self.currProfile]['src']
			dst=self.config[self.currProfile]['dst']
		else:
			src=utils.PathWinToUnix(self.config[self.currProfile]['src'])
			dst=utils.PathWinToUnix(self.config[self.currProfile]['dst'])	
		
		delete=self.config.getboolean(self.currProfile,'delete')
		history=self.config.getboolean(self.currProfile,'history')
		excludeFile=self.config[self.currProfile]['excludeFile']
		
		cmd=[rsyncBin, '-avh', '--info=progress2']
		if (delete==True): cmd.append('--delete')
		if (len(excludeFile)>1) : cmd.append("--exclude-from="+excludeFile)
		if (history==True): dst+=utils.getTimeHistoryFolder()
		cmd.append(src)
		cmd.append(dst)
		
		fileOutErr = open(utils.getTempDir()+"pobkup-errors.txt","w")
		print(cmd)
		if (not sys.platform == 'win32'): 
			self.proc = subprocess.Popen(cmd, bufsize=0 ,stdout=subprocess.PIPE, stderr=fileOutErr, shell=False)
		else:
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			self.proc = subprocess.Popen(cmd, bufsize=0 ,stdout=subprocess.PIPE, stderr=fileOutErr, startupinfo=si)
			
		while self.proc.poll() is None :
			out = self.proc.stdout.readline()
			
			#Print Output
			self.appendOutput(str(out.decode("utf-8")))
			#print(str(out.decode("utf-8")))
			
			#Print Progress
			if (self.getPercent(str(out.decode("utf-8"))) is not None):
				p=float(self.getPercent(str(out.decode("utf-8"))))
				wx.CallAfter(self.progress.SetValue,p)
				self.setStatus(_("Progress: ")+str(int(p))+'%')
				
		#Print error at the end
		if (os.stat(utils.getTempDir()+"pobkup-errors.txt").st_size != 0):
			fileOutErr= open(utils.getTempDir()+"pobkup-errors.txt","r")
			listErr=fileOutErr.readlines()
			for e in listErr:
				self.appendOutput(e)	
		
		#End of jobs
		fileOutErr.close()
		self.readyGui()
		self.imWorking=False
		self.appendOutput(_("BACKUP TERMINATED."))
		wx.CallAfter(self.progress.SetValue,100)
		self.setStatus(_("BACKUP TERMINATED."))
	
	
	
	def onStartStop(self, evt):
		#Check src and dest
		src=self.config[self.currProfile]['src']
		dst=self.config[self.currProfile]['dst']
		if (not utils.checkPath(src)):
			wx.CallAfter(Warn, self.frame, _("Source not present"), _("Warning"))
			self.readyGui()
			return
		if (not utils.checkPath(dst)):
			wx.CallAfter(Warn, self.frame, _("Destination not present"), _("Warning"))
			self.readyGui()
			return
		
		self.cleanOutput()
		self.progress.SetValue(0)
		
		
		if (self.imWorking==False):
			self.thdBackup = threading.Thread(target=self.startStopBackup)
			self.thdBackup.daemon = True
			self.thdBackup.start()
		else :
			self.proc.kill()
			self.readyGui()
			self.imWorking==False
			self.appendOutput(_("BACKUP TERMINATED BY USER."))
		
		
if __name__ == '__main__':
	
	#Gettext
	try:
		current_locale, encoding = locale.getdefaultlocale()
		locale_path = 'languages'
		language = gettext.translation ('pobkup', locale_path, [current_locale] )
		language.install()
	except:
		print("Locale not found")
		_ = gettext.gettext 
	
	utils.initConfig()
	app = MainApp(False)
	app.MainLoop()
