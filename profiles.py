#!/usr/bin/env python3
import wx,gettext, configparser,os,utils
from wx import xrc
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
		self.btSave=xrc.XRCCTRL(self.dialog, 'btSave')
		self.btDelete=xrc.XRCCTRL(self.dialog, 'btDelete')
		self.btCancel=xrc.XRCCTRL(self.dialog, 'btCancel')
		
		#Bind Widget Event
		self.btSave.Bind(wx.EVT_BUTTON, self.save)
		self.btDelete.Bind(wx.EVT_BUTTON, self.delete)
		self.btCancel.Bind(wx.EVT_BUTTON, self.closeWindow)
		
		self.dialog.Show()
	
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
	locale_path = 'languages'
	language = gettext.translation ('pobkup', locale_path, [current_locale] )
	language.install()
except:
	_ = gettext.gettext 
