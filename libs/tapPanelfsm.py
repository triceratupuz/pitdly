import wx
import fsm

class TapPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(TapPanel, self).__init__(*a, **k)#super the subclass
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		#BpM
		bpmT = wx.StaticText(self, -1, "Current B.p.M.", style= wx.ALIGN_LEFT)
		self.bpm = fsm.FsmCs(self, -1,
				digits=2,
				min_val = 10.0,
				max_val = 600,
				value = 60.0, 
				increment=0.01,
				cSound = self.cSound,
				channel = "gkbpm_to_cs")
		#Tap Tempo timer
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(100)
		self.Bind(wx.EVT_TIMER, self.updateBPM, self.timerRefresh)
		#Tap Tempo
		self.tiptap = 0
		self.tapTemnpB = wx.Button(self, -1, label='Tap Tempo')
		self.Bind(wx.EVT_BUTTON, self.sendTap, self.tapTemnpB)
		#Display
		mainSizer.Add(bpmT)
		mainSizer.Add(self.bpm)
		mainSizer.Add(self.tapTemnpB, -1, wx.ALL)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
	def OnClose(self, evt):
		self.timerRefresh.Stop()
		self.Destroy()
		
	
	def sendTap(self, evt):
		"""SendTap Event"""
		msg = 'i 4 0 -1'
		self.cSound.InputMessage(msg)
		bpm = self.cSound.GetChannel("gkbpm_from_cs")
		self.bpm.SetValue(bpm)
		
	
	def flashing(self):
		self.tiptap = (self.tiptap + 1) % 2
		if self.tiptap == 0:
			self.tapTemnpB.SetBackgroundColour('green')
		else:
			self.tapTemnpB.SetBackgroundColour('white')


	def updateBPM(self, evt):
		'''used by timer'''
		bpm = self.cSound.GetChannel("gkbpm_from_cs")
		self.bpm.SetValue(bpm)
		#print bpm



