#!/usr/bin/env python3
import wx,gettext,locale, configparser,os,utils
from wx import xrc
import wx.adv
from gui_utils import *

class Profiles(wx.Dialog):
	_profile=None
	
	def OnInit(self):
		self.res = xrc.XmlResource(os.path.join('gui','editProfiles.xrc'))
		self.init_dialog()
		
		return True

	def init_dialog(self):
		self.dialog = self.res.LoadDialog(None, 'mainDialogProfiles')
		self.txtLabel=xrc.XRCCTRL(self.dialog, 'txtLabel')
		self.dirPickerSrc=xrc.XRCCTRL(self.dialog, 'dirPickerSrc')
		self.dirPickerDst=xrc.XRCCTRL(self.dialog, 'dirPickerDst')
		self.chkDelete=xrc.XRCCTRL(self.dialog, 'chkDelete')
		self.chkHistory=xrc.XRCCTRL(self.dialog, 'chkHistory')
		self.filePickerExcludeFile=xrc.XRCCTRL(self.dialog, 'filePickerExcludeFile')
		self.filePickerLogFile=xrc.XRCCTRL(self.dialog, 'filePickerLogFile')
		self.txtCmdBefore=xrc.XRCCTRL(self.dialog, 'txtCmdBefore')
		self.txtCmdAfter=xrc.XRCCTRL(self.dialog, 'txtCmdAfter')
		
		self.spinEveryMinutes=xrc.XRCCTRL(self.dialog, 'spinEveryMinutes')
		self.spinEveryHours=xrc.XRCCTRL(self.dialog, 'spinEveryHours')
		self.chkEveryDayAt=xrc.XRCCTRL(self.dialog, 'chkEveryDayAt')
		self.chkEveryDayAt.SetValue(False)
		self.timePickerEveryDayAt=xrc.XRCCTRL(self.dialog, 'timePickerEveryDayAt')
		self.timePickerEveryDayAt.Enable(False)	
		
		
		self.btSave=xrc.XRCCTRL(self.dialog, 'btSave')
		self.btDelete=xrc.XRCCTRL(self.dialog, 'btDelete')
		self.btCancel=xrc.XRCCTRL(self.dialog, 'btCancel')
		
		#Bind Widget Event
		self.btSave.Bind(wx.EVT_BUTTON, self.save)
		self.btDelete.Bind(wx.EVT_BUTTON, self.delete)
		self.btCancel.Bind(wx.EVT_BUTTON, self.closeWindow)
		self.chkEveryDayAt.Bind(wx.EVT_CHECKBOX, self.enableDisableEveryDayAt)
		
		
		#Labels
		self.lblOperation=xrc.XRCCTRL(self.dialog, 'lblOperation')
		self.lblLabel=xrc.XRCCTRL(self.dialog, 'lblLabel')
		self.lblSrc=xrc.XRCCTRL(self.dialog, 'lblSrc')
		self.lblDst=xrc.XRCCTRL(self.dialog, 'lblDst')
		self.lblExcludeFile=xrc.XRCCTRL(self.dialog,'lblExcludeFile')
		
		self.lblOperation.SetLabel(_("Profile"))
		self.lblLabel.SetLabel(_("Label:"))
		self.lblSrc.SetLabel(_("Source:"))
		self.lblDst.SetLabel(_("Destination:"))
		self.chkDelete.SetLabel(_("Delete file from destination"))
		self.chkHistory.SetLabel(_("History"))
		self.lblExcludeFile.SetLabel(_("Exclude path from file:"))
		self.btSave.SetLabel(_("Save"))
		self.btDelete.SetLabel(_("Delete"))
		self.btCancel.SetLabel(_("Cancel"))
	
	def enableDisableEveryDayAt(self, evt):
		if (self.chkEveryDayAt.IsChecked()):
			self.timePickerEveryDayAt.Enable(True)	
		else:
			self.timePickerEveryDayAt.Enable(False)
			
	def closeWindow(self, evt):
		self.dialog.Close()
	
	def setProfile(self,p):
		self._profile=p
		self.loadProfile(self._profile)
	
	def loadProfile(self,p):
		self.config = configparser.ConfigParser()
		self.config.read(utils.getProfilesFilePath())
		
		self.txtLabel.SetValue(p)
		self.dirPickerSrc.SetPath(self.config[p]['src'])
		self.dirPickerDst.SetPath(self.config[p]['dst'])
		if (self.config[p]['delete']=='yes'): self.chkDelete.SetValue(True)
		if (self.config[p]['history']=='yes'): self.chkHistory.SetValue(True)
		self.filePickerExcludeFile.SetPath(self.config[p]['excludeFile'])
		self.filePickerLogFile.SetPath(self.config[p]['logfile'])
		self.txtCmdBefore.SetValue(self.config[p]['cmdbefore'])
		self.txtCmdAfter.SetValue(self.config[p]['cmdafter'])
		
		try:
			self.spinEveryMinutes.SetValue(self.config[p]['everyMinutes'])
			self.spinEveryHours.SetValue(self.config[p]['everyHours'])
		except:
			pass
			
		try:
			if (self.config[p]['everyDayAt']!=None and self.config[p]['everyDayAt']!=""):
				time=self.config[p]['everyDayAt'].split(':')
				hours=int(time[0])
				mins=int(time[1])
				secs=int(time[2])
				self.timePickerEveryDayAt.SetTime(hours,mins,secs)
				self.chkEveryDayAt.SetValue(True)
				self.timePickerEveryDayAt.Enable(True)
		except:
			pass		
			
	
	def save(self,evt):
		try:
			self.config = configparser.ConfigParser()
			self.config.read(utils.getProfilesFilePath())
			
			self.config.remove_section(self._profile)
			self.config.add_section(self.txtLabel.GetValue())
			
			self.config[self.txtLabel.GetValue()]['src'] = self.dirPickerSrc.GetPath()
			self.config[self.txtLabel.GetValue()]['dst'] = self.dirPickerDst.GetPath()
			if(self.chkDelete.IsChecked()):
				self.config[self.txtLabel.GetValue()]['delete'] = "yes"
			else:
				self.config[self.txtLabel.GetValue()]['delete'] = "no"	
			if(self.chkHistory.IsChecked()):
				self.config[self.txtLabel.GetValue()]['history'] = "yes"
			else:
				self.config[self.txtLabel.GetValue()]['history'] = "no"
			self.config[self.txtLabel.GetValue()]['excludeFile'] = self.filePickerExcludeFile.GetPath()
			self.config[self.txtLabel.GetValue()]['logfile'] = self.filePickerLogFile.GetPath()
			self.config[self.txtLabel.GetValue()]['cmdbefore'] = self.txtCmdBefore.GetValue()
			self.config[self.txtLabel.GetValue()]['cmdafter'] = self.txtCmdAfter.GetValue()
			
			if (self.spinEveryMinutes.GetValue()>0): self.config[self.txtLabel.GetValue()]['everyMinutes'] = str(self.spinEveryMinutes.GetValue())
			if(self.spinEveryHours.GetValue()>0): self.config[self.txtLabel.GetValue()]['everyHours'] = str(self.spinEveryHours.GetValue())
			
			if(self.chkEveryDayAt.IsChecked()):
				hours=str(self.timePickerEveryDayAt.GetTime()[0])
				mins=str(self.timePickerEveryDayAt.GetTime()[1])
				secs=str(self.timePickerEveryDayAt.GetTime()[2])
				self.config[self.txtLabel.GetValue()]['everyDayAt'] = "%s:%s:%s" % (hours, mins,secs)
				
		
			with open(utils.getProfilesFilePath(), 'w') as configfile:
				self.config.write(configfile)
		
			self.dialog.Close()
		except  :
			Warn(self.dialog, _("Error on save profile"), caption = _('Warning!'))
	
	def delete(self,evt):
		try:
			r= YesNo(self.dialog, _("Do you want delete the profile?"), caption = _('Warning'))
			if (r==False): return 
			
			self.config = configparser.ConfigParser()
			self.config.read(utils.getProfilesFilePath())
			self.config.remove_section(self._profile)
			with open(utils.getProfilesFilePath(), 'w') as configfile:
				self.config.write(configfile)
			self.dialog.Close()
		except  ConfigParser.NoSectionError:
			Warn(self.dialog, _("Error on delete profile"), caption = _('Warning!'))			

#Gettext
try:
	current_locale, encoding = locale.getdefaultlocale()
	locale_path = 'locale'
	language = gettext.translation ('pobkup', locale_path, [current_locale] )
	language.install()
except:
	_ = gettext.gettext 
