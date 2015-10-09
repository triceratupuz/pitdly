import wx
import txtctrlnum

class TapPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(TapPanel, self).__init__(*a, **k)#super the subclass
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		#BpM
		bpmT = wx.StaticText(self, -1, "Current B.p.M.", style= wx.ALIGN_LEFT)
		self.bpm = txtctrlnum.TxtCtrlNumCs(self, -1,
				style=wx.TE_PROCESS_ENTER|wx.TE_RICH2,
				min_val = 10.0,
				max_val = 600,
				init_val = 60.0, cSound = self.cSound,
				channel = "gkbpm_to_cs")
		#Tap Tempo
		self.altcol = 0
		self.tapTemnpB = wx.Button(self, -1, label='Tap Tempo')
		
		#Display
		mainSizer.Add(bpmT)
		mainSizer.Add(self.bpm)
		mainSizer.Add(self.tapTemnpB)
		#mainSizer.Add(self.gridPan, 0)
		#mainSizer.Add(controlSizer, 1, wx.ALL)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		#timer to update the value of the Bpm if tap tempo
		self.timer = wx.Timer(self, wx.ID_ANY)
		self.Bind(wx.EVT_TIMER, self.updateBPM, self.timer)
		
		#Bindings
		#self.Bind(wx.EVT_IDLE, self.readMetro)#Receive metromome and update gui
		self.Bind(wx.EVT_BUTTON, self.sendTap, self.tapTemnpB)#Send tap tempo events
		
	
	
	def sendTap(self, evt):
		"""SendTap Event"""
		msg = 'i 3 0 -1'
		self.cSound.InputMessage(msg)
		bpm = self.cSound.GetChannel("gkbpm_from_cs")
		self.bpm.SetValueC(bpm)
		self.timer.Start(100)

	def updateBPM(self, evt):
		bpm = self.cSound.GetChannel("gkbpm_from_cs")
		self.bpm.SetValueC(bpm)
		self.timer.Stop()
		evt.Skip()
		#print bpm

	def readMetro(self, evt):
		"""not working properly does not sync
		Binding removed for wx.EVT_IDLE, it's not called
		"""
		tick = self.cSound.GetChannel("metro_from_cs")
		#print tick
		if tick == 1:
			self.altcol = (self.altcol + 1) % 2
			self.tapTemnpB.SetBackgroundColour((220 * (1-self.altcol), 220 * (self.altcol), 100))
		evt.RequestMore()
		evt.Skip()
		
	def readMetroC(self):
		#must be called by callback"
		tick = self.cSound.GetChannel("metro_from_cs")
		#print tick
		if tick == 1:
			self.altcol = (self.altcol + 1) % 2
			self.tapTemnpB.SetBackgroundColour((220 * (1-self.altcol), 220 * (self.altcol), 100))
	
	def readMetroB(value):
		#must be called by callback"
		#tick = self.cSound.GetChannel("metro_from_cs")
		print value
		"""
		if tick == 1:
			self.altcol = (self.altcol + 1) % 2
			self.tapTemnpB.SetBackgroundColour((220 * (1-self.altcol), 220 * (self.altcol), 100))
		"""
	
	def stampatest(self):
		print "stampatest"

class TxtCtrlNumCsyyy(txtctrlnum.TxtCtrlNum):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(TxtCtrlNumCs, self).__init__(*a, **k)#super the subclass


	def checkValueKey(self, evt):
		"""keyboard input 
		Added csound send to the original class
		non need to Bins since binding is in the parent class
		"""
		self.edita = 0
		self.SetForegroundColour(self.colWaitConf)
		keycode = evt.GetKeyCode()
		if keycode == wx.WXK_RETURN or keycode == wx.WXK_NUMPAD_ENTER: 
			try:
				self.init_val = float(self.GetValue())
				self.rangechk()
				self.ChangeValue(self.init_valStr)
				self.oldvalue = self.init_val
			except ValueError:
				self.init_val = self.oldvalue
				self.ChangeValue(self.init_valStr)
			self.SetForegroundColour(self.foregroundcolour)
			self.edita = 1
		#print "key edita = %i value = %f" % (self.edita, self.init_val)
		self.cSound.SetChannel("gkbpm_to_cs", self.init_val)
		evt.Skip()
		
		
	def onMouseWheel(self, evt):
		"""mouse wheeel input
		Added csound send to the original class
		non need to Bins since binding is in the parent class
		"""
		self.edita = 0
		#print evt.GetWheelDelta()
		wheel_rotation = evt.GetWheelRotation() / 120.0
		self.init_val = wheel_rotation * (self.max_val - self.min_val) * self.mwhs + self.init_val
		self.rangechk()
		self.ChangeValue(self.init_valStr)
		self.oldvalue = self.init_val
		self.edita = 1
		#print self.init_val
		self.cSound.SetChannel("gkbpm_to_cs", self.init_val)
		evt.Skip()

