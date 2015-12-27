#!/usr/bin/python

import wx
import os
import csnd6
import math
import libs.tapPanel as tapPanel
import libs.dlyPanel as dlyPanel
import libs.singledlyPanel as singledlyPanel
import libs.presetPanel as presetPanel

#CSND CODE###########################################################
###################################################################
###################################################################
c = csnd6.Csound()    # create an instance of Csound

file = "csd/TPZ_seqpitdly_pvspit_low_reso.csd"

c.Compile(file)     # Compile Orchestra from String

# SET CHANNELS HERE

def updateMetronome(csound):
	"""update gui metronome"""
	tick = csound.GetChannel("metro_from_cs")
	#frame.tapP.readMetroB(tick)
	#print frame.tapP.stampatest()

perfThread = csnd6.CsoundPerformanceThread(c)

# SET CALLBACKS HERE
perfThread.SetProcessCallback(updateMetronome, c) 

#performance thread
perfThread.Play()


#GUI CODE###########################################################
###################################################################
###################################################################
#Frame
class TopFrame(wx.Frame):
	"""Main frame"""
	#def __init__(self, *a, **k):
	def __init__(self, parent, title):
		#wx.Frame.__init__(self, *a, **k)
		#self.csound = k.pop('csound', None)
		#super(TopFrame, self).__init__(*a, **k)#super the subclass
		super(TopFrame, self).__init__(parent= parent, title = title, size=(1090, 670))#super the subclass
		#menu under ubuntu problems with menus
		#self.topMenu()
		#create the items
		#tap panel
		self.tapP = tapPanel.TapPanel(self, -1, (-1,-1), cSound=c, cSound_perf=perfThread)
		#delay panel
		self.matrixSeqP = dlyPanel.DlyPanel(self, -1, (-1,-1), cSound=c, cSound_perf=perfThread)
		self.matrixSeqP.SetBackgroundColour((0, 250, 2))
		#dealu 
		self.singledlyP = singledlyPanel.SingleDlyPanel(self, -1, (-1,-1), cSound=c, cSound_perf=perfThread)
		
		#Preset
		self.presetP = presetPanel.PresetPanel(self, -1, (-1,-1), cSound=c, cSound_perf=perfThread)
		#self.presetP.SetBackgroundColour((250, 0, 0))
		#create the sizer
		self.vboxsizer = wx.BoxSizer(wx.VERTICAL)
		#add in the sizer
		self.vboxsizer.Add(self.tapP, 0,flag=wx.EXPAND)
		self.vboxsizer.Add(self.matrixSeqP, 0,flag=wx.EXPAND)
		self.vboxsizer.Add(self.singledlyP, 0,flag=wx.EXPAND)
		self.vboxsizer.Add(self.presetP, -1,flag=wx.EXPAND)
		#set sizer to panel
		#self.SetSizeHints(800, 300)
		#self.SetSize(wx.Size(800, 300))
		self.SetSizer(self.vboxsizer)
		#self.vboxsizer.Fit(self)
		
		self.Show()


	def OnClose(self, event):
		"""to stop all the timers created"""
		#self.tapP.timerFlash.Stop()
		self.matrixSeqP.inPanel.timerRefresh.Stop() 
		self.matrixSeqP.dlyPanel.timerRefresh.Stop() 
		self.Destroy()
		
	


class AppWithTerm(wx.App):
	"""wx.App subclassed to include csound Thread termination"""
	def OnExit(self):
		#print "Closing csnd Thread"
		perfThread.Stop()
		perfThread.Join()
		#print "Closed csnd Thread"


app = AppWithTerm(False)#True to redirect stdin/sterr
frame = TopFrame(None, title='Pitdly')
app.MainLoop()

