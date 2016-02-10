import wx
import fsm

class InputPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(InputPanel, self).__init__(*a, **k)#super the subclass
		self.SetBackgroundColour((200, 200, 200))
		siz=wx.Size(70,-1)#size of floatspin
		#Mono Stereo Input Selector
		self.monoStereo = wx.CheckBox(self, -1, label='StereoIn', style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.monoStereoSelect, self.monoStereo)
		#VUMETER
		self.vuSizer  = wx.GridBagSizer(vgap=10, hgap=10)
		vuLT = wx.StaticText(self, -1, "dB L", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inL = wx.TextCtrl(self, -1, size=(60,20))
		vuRT = wx.StaticText(self, -1, "dB R", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inR = wx.TextCtrl(self, -1, size=(60,20))
		#Gain
		gainT = wx.StaticText(self, -1, "Gain", style= wx.ALIGN_LEFT)
		self.gain = fsm.FsmTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.001,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 11)#channel = "inGainDly"
		#Test Sound
		self.testSound = wx.CheckBox(self, -1, label='test Sound', style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.testSoundSelect, self.testSound)
		#Timer Update MUST BE STOPPED ON CLOSE
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(200)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)
		#initialize values
		self.cSound.TableSet(99, 0, 0.0)
		self.cSound.TableSet(99, 11, 1.0)
		#Recycle Stuff
		RecycleT = wx.StaticText(self, -1, "Recycle", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.Recycle = wx.StaticText(self, -1, "Off", style= wx.ALIGN_CENTER | wx.TE_RICH)
		#time_index = 2
		#time_index = 1
		timeT = wx.StaticText(self, -1, "Time:", style= wx.ALIGN_RIGHT)
		#self.timeV= str(self.cSound.TableGet(self.tabN, 1))
		self.timeV= "0"
		self.time = wx.StaticText(self, -1, self.timeV, style= wx.ALIGN_LEFT)
		#feed_index = 2
		feedT = wx.StaticText(self, -1, "Feedback", style= wx.ALIGN_RIGHT)
		self.feed = fsm.FsmTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 1.0,
																			increment=0.001,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 2)
		self.feed.SetValue(self.cSound.TableGet(99, 2))
		#recycle HP_index = 5
		recycleHPT = wx.StaticText(self, -1, "MinFreq", style= wx.ALIGN_RIGHT)
		self.recycleHP = fsm.FsmTs(parent=self, id=-1,
																			digits=3,
																			min_val = 20.0,
																			max_val = 22500.0,
																			increment=1.0,
																			value = 20.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 5)
		self.recycleHP.SetValue(self.cSound.TableGet(99, 5))
		#recycle LP_index = 6
		recycleLPT = wx.StaticText(self, -1, "MaxFreq", style= wx.ALIGN_RIGHT)
		self.recycleLP = fsm.FsmTs(parent=self, id=-1,
																			digits=3,
																			min_val = 20.0,
																			max_val = 22500.0,
																			increment=1.0,
																			value = 22500.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 6)
		self.recycleLP.SetValue(self.cSound.TableGet(99, 6))
		#recicle input direct index = 3
		recycleInT = wx.StaticText(self, -1, "Direct In", style= wx.ALIGN_RIGHT)
		self.recycleIn = fsm.FsmTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 2.0,
																			increment=0.001,
																			value = 0.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 3)
		self.recycleIn.SetValue(self.cSound.TableGet(99, 3))
		#Sizer
		self.vuSizer.Add(self.monoStereo, pos=(0,1))
		self.vuSizer.Add(vuLT, pos=(2,0))
		self.vuSizer.Add(self.vumeter_inL, pos=(2,1))
		self.vuSizer.Add(vuRT, pos=(3,0))
		self.vuSizer.Add(self.vumeter_inR, pos=(3,1))
		self.vuSizer.Add(gainT, pos=(1,0))
		self.vuSizer.Add(self.gain, pos=(1,1))
		self.vuSizer.Add(self.testSound, pos=(4,1))
		#Recycle in the sizer
		self.vuSizer.Add(RecycleT, pos=(6,0))
		self.vuSizer.Add(self.Recycle, pos=(6,1))
		self.vuSizer.Add(timeT, pos=(7,0))
		self.vuSizer.Add(self.time, pos=(7,1))
		self.vuSizer.Add(recycleInT, pos=(8,0))
		self.vuSizer.Add(self.recycleIn, pos=(8,1))
		self.vuSizer.Add(feedT, pos=(9,0))
		self.vuSizer.Add(self.feed, pos=(9,1))
		self.vuSizer.Add(recycleHPT, pos=(10,0))
		self.vuSizer.Add(self.recycleHP, pos=(10,1))
		self.vuSizer.Add(recycleLPT, pos=(11,0))
		self.vuSizer.Add(self.recycleLP, pos=(11,1))
		#
		self.SetSizer(self.vuSizer)
		self.vuSizer.Fit(self)


	def onClose(self, evt):
		self.timerRefresh.Stop() 
		self.Destroy()



	def monoStereoSelect(self, evt):
		state = self.monoStereo.IsChecked()
		if state:
			#self.cSound.SetChannel("monostereo", 1.0)
			self.cSound.TableSet(99, 0, 1.0)
		else:
			#self.cSound.SetChannel("monostereo", 0.0)
			self.cSound.TableSet(99, 0, 0.0)

	def testSoundSelect(self, evt):
		state = self.testSound.IsChecked()
		if state:
			self.cSound.SetChannel("test_sound", 1)
			#self.cSound.InputMessage("i 2 0 1")
		else:
			self.cSound.SetChannel("test_sound", 0)
		#print state
		
	def timerUpdate(self, evt):
		"""update the vumeters"""
		self.dbL = self.cSound.GetChannel("directvul")
		self.dbR = self.cSound.GetChannel("directvur")
		if self.dbL < -1.0:
			self.vumeter_inL.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbL < 0.0:
			self.vumeter_inL.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_inL.SetForegroundColour((250, 10, 10))
		if self.dbR < -1.0:
			self.vumeter_inR.SetForegroundColour((100,250, 100))
		elif -1.0<= self.dbR < 0.0:
			self.vumeter_inR.SetForegroundColour((250, 200, 0))
		else:
			self.vumeter_inR.SetForegroundColour((250, 10, 10))
		self.vumeter_inL.SetValue(str(self.dbL))
		self.vumeter_inR.SetValue(str(self.dbR))
		

	def updateGraphics(self, recycleStatus, delaytime):
		self.Recycle.SetLabel(recycleStatus)
		self.time.SetLabel("%.3f" % (delaytime))
		self.vuSizer.Layout()