import wx
import floatspinmouse
import inputPanel
import gridPanel

class DlyPanel(wx.Panel):
	def __init__(self, *a, **k):
		self.cSound = k.pop('cSound', None)
		self.cSound_perf = k.pop('cSound_perf', None)
		super(DlyPanel, self).__init__(*a, **k)#super the subclass
		mainSizer = wx.BoxSizer(wx.HORIZONTAL)
		controlSizer = wx.GridBagSizer(vgap=5, hgap=5)
		self.dcw, self.dch = 750, 530
		self.buttw = 30
		siz=wx.Size(70,-1)#size of floatspin
		#bkw button
		self.bkwbttn = wx.Button(self, -1, label='<<', size = (self.buttw, self.dch))
		#self.startOnDc = 0
		#fwd
		self.fwdbttn = wx.Button(self, -1, label='>>', size = (self.buttw, self.dch))
		
		self.stepsDict = {"1":1.0,
									"1/8":.5,
									"1/8T":.5 * 2/3,
									"1/16":.25,
									"1/16T":.25 * 2/3,
									"1/32":.125,
									"1/32T":.125 * 2/3,
									"1/64":.0625}
		self.stepsIndex = "1/8"
		self.stepsMultiplier = self.stepsDict[self.stepsIndex]
		self.stepsNames = self.stepsDict.keys()
		self.Stepvalue = wx.ComboBox(self, -1, choices=self.stepsNames, size=wx.Size(60, 20))
		self.Bind(wx.EVT_COMBOBOX, self.timeGridSetting, self.Stepvalue)
		self.Stepvalue.SetValue(self.stepsIndex)
		
		stepValueT = wx.StaticText(self, -1, "Time\nDiv", style = wx.ALIGN_LEFT)
		
		timeqtT = wx.StaticText(self, -1, "Time\nQuant", style= wx.ALIGN_LEFT)
		self.timeQt = wx.CheckBox(self, -1, style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.timeQuantizeSet, self.timeQt)
		
		pitqtT = wx.StaticText(self, -1, "Pitch\nQuant", style= wx.ALIGN_LEFT)
		self.pitQt = wx.CheckBox(self, -1, style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.pitQuantizeSet, self.pitQt)
		
		
		self.zoomIn = wx.Button(self, -1, label='Zoom In', size=(60,20))
		self.zoomOut = wx.Button(self, -1, label='Zoom Out', size=(60,20))
		
		gainTI = wx.StaticText(self, -1, "Gain\nDirect", style= wx.ALIGN_LEFT)
		self.gainI = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.001,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 7)#channel = "outdirectV"
		
		gainTD = wx.StaticText(self, -1, "Gain\nDelay", style= wx.ALIGN_LEFT)
		self.gainD = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.001,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 8)#channel = "outdlyV"
		
		gainTR = wx.StaticText(self, -1, "Gain\nRecycle", style= wx.ALIGN_LEFT)
		self.gainR = floatspinmouse.FloatSpinMouseTs(parent=self, id=-1,
																			digits=3,
																			min_val = 0.0,
																			max_val = 10.0,
																			increment=0.001,
																			value = 1.0,
																			size = siz,
																			cSound = self.cSound,
																			ftable = 99,
																			indxn = 9)#channel = "outrecycV"
		
		#Limiter
		limitT = wx.StaticText(self, -1, "Limiter", style= wx.ALIGN_LEFT)
		self.limit = wx.CheckBox(self, -1, style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.limitSet, self.limit)
		
		#VUMETER
		vuLT = wx.StaticText(self, -1, "dB L", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inL = wx.TextCtrl(self, -1, size=(60,20))
		vuRT = wx.StaticText(self, -1, "dB R", style= wx.ALIGN_CENTER | wx.TE_RICH)
		self.vumeter_inR = wx.TextCtrl(self, -1, size=(60,20))
		
		#Timer Update MUST BE STOPPED IN MAIN FRAME
		self.timerRefresh = wx.Timer(self, wx.ID_ANY)
		self.timerRefresh.Start(200)
		self.Bind(wx.EVT_TIMER, self.timerUpdate, self.timerRefresh)
		
		bord = 12
		controlSizer.Add(stepValueT, pos=(0,0))
		controlSizer.Add(self.Stepvalue, pos=(0,1))
		controlSizer.Add(timeqtT, pos=(1,0))
		controlSizer.Add(self.timeQt, pos=(1,1))
		controlSizer.Add(pitqtT, pos=(2,0))
		controlSizer.Add(self.pitQt, pos=(2,1))
		controlSizer.Add(self.zoomIn, pos=(3,1))
		controlSizer.Add(self.zoomOut, pos=(4,1))
		
		controlSizer.Add(gainTI, pos=(7,0))
		controlSizer.Add(self.gainI, pos=(7,1))
		controlSizer.Add(gainTD, pos=(8,0))
		controlSizer.Add(self.gainD, pos=(8,1))
		controlSizer.Add(gainTR, pos=(9,0))
		controlSizer.Add(self.gainR, pos=(9,1))
		controlSizer.Add(limitT, pos=(10,0))
		controlSizer.Add(self.limit, pos=(10,1))
		controlSizer.Add(vuLT, pos=(11,0))
		controlSizer.Add(self.vumeter_inL, pos=(11,1))
		controlSizer.Add(vuRT, pos=(12,0))
		controlSizer.Add(self.vumeter_inR, pos=(12,1))
		
		#Dly DC panel
		self.gridPan = gridPanel.GridPanel(self, -1, dcw = self.dcw, dch = self.dch, stepsDict = self.stepsDict,  cSound=self.cSound, cSound_perf=self.cSound_perf)
		self.gridPan.SetSize(wx.Size(self.dcw, self.dch))
		
		#inputPanel
		self.inPanel = inputPanel.InputPanel(self, -1,  cSound=self.cSound, cSound_perf=self.cSound_perf)
		
		#Display
		mainSizer.Add(self.inPanel,0,flag=wx.EXPAND)
		mainSizer.Add(self.bkwbttn,0,flag=wx.EXPAND)
		mainSizer.Add(self.gridPan, 0)
		mainSizer.Add(self.fwdbttn, 0,flag=wx.EXPAND)
		mainSizer.Add(controlSizer, 0, flag=wx.EXPAND)
		#mainSizer.Add(self.outPanel,-1,flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		#Bindings
		self.Bind(wx.EVT_BUTTON, self.gridPan.setStartOnDc_m, self.bkwbttn)#decrease staritng point
		self.Bind(wx.EVT_BUTTON, self.gridPan.setStartOnDc_p, self.fwdbttn)#increase starting point
		self.Bind(wx.EVT_BUTTON, self.gridPan.setZoom_in, self.zoomIn)#increase starting point
		self.Bind(wx.EVT_BUTTON, self.gridPan.setZoom_out, self.zoomOut)#increase starting point
		
		#initialize values
		#self.cSound.SetChannel("outdirectV", 1.0)
		#self.cSound.SetChannel("outdlyV", 1.0)
		#self.cSound.SetChannel("outrecycV", 1.0)
		self.cSound.TableSet(99, 7, 1.0)
		self.cSound.TableSet(99, 8, 1.0)
		self.cSound.TableSet(99, 9, 1.0)
		self.cSound.TableSet(99, 10, 0.0)


	def timeGridSetting(self, evt):
		"""set the grid divisor"""
		#print self.stepsNames[self.Stepvalue.GetSelection()]
		self.gridPan.stepsIndex = self.stepsNames[self.Stepvalue.GetSelection()]
		self.gridPan.timeGridSetting(evt)


	def timeQuantizeSet(self, evt):
		"""time quantization checkbox managing"""
		self.gridPan.timeQuantize = self.timeQt.GetValue()
		
	def pitQuantizeSet(self, evt):
		"""pitch quantization checkbox managing"""
		self.gridPan.pitcQuantize = self.pitQt.GetValue()
	
	def limitSet(self, evt):
		"""activate the limiter"""
		state = self.limit.IsChecked()
		if state:
			#self.cSound.SetChannel("limitON", 1.0)
			self.cSound.TableSet(99, 10, 1.0)
		else:
			#self.cSound.SetChannel("limitON", 0.0)
			self.cSound.TableSet(99, 10, 0.0)


	def timerUpdate(self, evt):
		"""update the vumeters"""
		self.dbL = self.cSound.GetChannel("totalvul")
		self.dbR = self.cSound.GetChannel("totalvur")
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